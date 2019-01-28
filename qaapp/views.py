from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, DetailView

from qaapp.forms import QuestionCreateForm
from qaapp.models import Question


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


class QuestionDetailsView(DetailView):
    model = Question
    template_name = 'questions/show.html'
