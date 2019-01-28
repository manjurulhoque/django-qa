from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, DetailView

from qaapp.forms import QuestionCreateForm
from qaapp.models import Question


def handler404(request):
    return render(request, '404.html', status=404)


class QuestionListView(ListView):
    model = Question
    queryset = Question.objects.all()
    context_object_name = "questions"
    template_name = 'home.html'
    paginate_by = 6

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


class QuestionDetailsView(DetailView):
    model = Question
    template_name = 'questions/show.html'
    context_object_name = 'question'
    queryset = Question.objects.all()

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
        return context
