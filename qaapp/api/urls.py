from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import QuestionViewSet, QuestionFavoriteViewSet
from . import views

router = DefaultRouter()
router.register('question', QuestionViewSet, base_name='questions')
router.register(r'question/(?P<question_id>\d+)/favorites', QuestionFavoriteViewSet, base_name='questions-favorites')

urlpatterns = [
    path('questions/', views.QuestionListApiView.as_view()),
    path('questions/<int:question_id>/<str:flag>', views.question_vote),
]

urlpatterns += router.urls
