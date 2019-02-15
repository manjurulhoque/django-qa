from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import QuestionViewSet
from . import views

router = DefaultRouter()
router.register('question', QuestionViewSet, base_name='questions')

urlpatterns = [
    path('questions/', views.QuestionListApiView.as_view()),
]

urlpatterns += router.urls
