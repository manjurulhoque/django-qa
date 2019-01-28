from django.urls import path

from qaapp.views import QuestionDetailsView
from . import views

app_name = 'qa'

urlpatterns = [
    path('', views.QuestionListView.as_view(), name='home'),
    path('questions/<slug:slug>/', QuestionDetailsView.as_view(), name='questions-detail'),
    path('questions/create', views.QuestionCreateView.as_view(), name='questions-create')
]
