from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.http import Http404, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from django.views.generic.edit import FormMixin, DeleteView
from django.views.generic import View

from qaapp.forms import QuestionCreateForm, AnswerCreateForm
from qaapp.models import Question, QuestionVote, Answer


def handler404(request):
    return render(request, '404.html', status=404)


class QuestionListView(ListView):
    model = Question
    queryset = Question.objects.all()
    context_object_name = "questions"
    template_name = 'home.html'
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Home'
        return context


class QuestionCreateView(CreateView):
    form_class = QuestionCreateForm
    extra_context = {
        'title': 'Create Question'
    }
    template_name = 'questions/create.html'
    success_url = '/'

    @method_decorator(login_required(login_url='/login'))
    def dispatch(self, *args, **kwargs):
        return super(QuestionCreateView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(QuestionCreateView, self).form_valid(form)


class QuestionDetailsView(FormMixin, DetailView):
    model = Question
    template_name = 'questions/show.html'
    context_object_name = 'question'
    queryset = Question.objects.all()
    form_class = AnswerCreateForm

    def get(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
        except Http404:
            # redirect here
            raise Http404("Question doesn't exists")
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def get_object(self, queryset=None):
        obj = super(QuestionDetailsView, self).get_object(queryset=queryset)
        if obj is None:
            raise Http404("Question doesn't exists")
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.get_object().title
        context['votes_count'] = self.get_object().question_votes.aggregate(Sum('vote'))
        if self.request.user.is_authenticated:
            vote = self.request.user.question_votes.filter(question_id=self.get_object().id).first()
            if vote:
                context['voted'] = True
                if vote.vote == 1:
                    context['vote_type'] = 'upvote'
                else:
                    context['vote_type'] = 'downvote'
            else:
                context['voted'] = False
        else:
            context['voted'] = False
        return context

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('qa:questions-detail', kwargs={'slug': self.get_object().slug})

    def form_valid(self, form):
        # save comment
        form.instance.user = self.request.user
        form.instance.question = self.get_object()
        form.instance.body = form.cleaned_data["body"]
        form.save()
        return super().form_valid(form)


class QuestionUpdateView(UpdateView):
    model = Question
    template_name = 'questions/edit.html'
    form_class = QuestionCreateForm
    context_object_name = 'question'
    queryset = Question.objects.all()
    slug_field = 'slug'

    def get_object(self, queryset=None):
        """
            Return the object the view is displaying.
            Require `self.queryset` and a `pk` or `slug` argument in the URLconf.
            Subclasses can override this to return any object.
            """
        # Use a custom queryset if provided; this is required for subclasses
        # like DateDetailView
        if queryset is None:
            queryset = self.get_queryset()
        # Next, try looking up by primary key.
        pk = self.kwargs.get(self.pk_url_kwarg)
        slug = self.kwargs.get(self.slug_url_kwarg)
        if pk is not None:
            queryset = queryset.filter(pk=pk)
        # Next, try looking up by slug.
        if slug is not None and (pk is None or self.query_pk_and_slug):
            slug_field = self.get_slug_field()
            queryset = queryset.filter(**{slug_field: slug})
        # If none of those are defined, it's an error.
        if pk is None and slug is None:
            raise AttributeError(
                "Generic detail view %s must be called with either an object "
                "pk or a slug in the URLconf." % self.__class__.__name__
            )
        try:
            # Get the single item from the filtered queryset
            obj = queryset.get()
        except queryset.model.DoesNotExist:
            raise Http404("No question found matching the query")
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.get_object().title
        return context

    def get_success_url(self):
        return reverse_lazy('qa:questions-detail', kwargs={'slug': self.get_object().slug})

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(QuestionUpdateView, self).form_valid(form)


class QuestionDestroyView(DeleteView):
    model = Question
    success_url = reverse_lazy('qa:home')
    context_object_name = 'question'


@login_required(login_url='/login')
def question_vote(request, question_id=None, flag='upvote'):
    # print(flag, question_id)
    # return redirect(reverse_lazy('qa:home'))
    question = Question.objects.get(id=question_id)
    if request.method == 'POST':
        if request.user.is_authenticated:
            if QuestionVote.objects.filter(user=request.user, question=question).exists():  # check if exists
                vote = QuestionVote.objects.get(user=request.user, question=question)
                if vote.vote == -1 and flag == 'upvote':  # if down vote and request for upvote
                    vote.vote = 1
                    vote.save()
                elif vote.vote == 1 and flag == 'upvote':  # if already given upvote and want to remove the upvote
                    vote.delete()
                    return redirect(reverse_lazy('qa:questions-detail', kwargs={'slug': question.slug}))
                elif vote.vote == -1 and flag == 'downvote':  # if already given downvote and want to remove the downvote
                    vote.delete()
                    return redirect(reverse_lazy('qa:questions-detail', kwargs={'slug': question.slug}))
                else:  # if already downvote and want to upvote
                    vote.vote = 1
                    vote.save()
                return redirect(reverse_lazy('qa:questions-detail', kwargs={'slug': question.slug}))
            else:
                vote = QuestionVote()
                vote.user = request.user
                vote.question = question
                if flag == 'upvote':
                    vote.vote = 1
                else:
                    vote.vote = -1
                vote.save()
                return redirect(reverse_lazy('qa:questions-detail', kwargs={'slug': question.slug}))
    else:
        return redirect(reverse_lazy('qa:questions-detail', kwargs={'slug': question.slug}))


@login_required(login_url='/login')
def mark_as_best(request, question_id=None, answer_id=None):
    question = Question.objects.get(id=question_id)
    answer = Answer.objects.get(id=answer_id)
    if request.method == 'POST' and question.user == request.user:
        question.best_answer = answer
        question.save()
        return redirect(reverse_lazy('qa:questions-detail', kwargs={'slug': question.slug}))
    else:
        return redirect(reverse_lazy('qa:questions-detail', kwargs={'slug': question.slug}))
