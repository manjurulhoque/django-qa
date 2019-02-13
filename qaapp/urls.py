from django.urls import path

from qaapp.views import QuestionDetailsView
from . import views

app_name = 'qa'

urlpatterns = [
    path('', views.QuestionListView.as_view(), name='home'),
    path('questions/<slug:slug>/', QuestionDetailsView.as_view(), name='questions-detail'),
    path('questions/create', views.QuestionCreateView.as_view(), name='questions-create'),
    path('questions/<slug:slug>/edit', views.QuestionUpdateView.as_view(), name='questions-edit'),
    path('questions/<slug:slug>/delete', views.QuestionDestroyView.as_view(), name='questions-delete'),
    path('questions/<int:question_id>/<str:flag>', views.question_vote, name='questions-vote'),
    # answer
    path('answers/<int:question_id>/<int:answer_id>/best_answer', views.mark_as_best, name='mark-as-best'),
]
