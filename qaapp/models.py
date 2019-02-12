from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.utils import timezone


class Answer(models.Model):
    question = models.ForeignKey('Question', on_delete=models.SET_NULL, null=True, blank=True, related_name='answer')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='answer')
    body = models.TextField()
    created_at = models.DateTimeField(verbose_name='Created At', default=timezone.now)
    updated_at = models.DateTimeField(verbose_name='Updated At', default=timezone.now)


class Question(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='questions')
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    body = models.TextField()
    views = models.IntegerField(verbose_name='Page Views', default=0)
    best_answer = models.OneToOneField(Answer, null=True, blank=True, on_delete=models.SET_NULL,
                                       related_name='best_answer')
    created_at = models.DateTimeField(verbose_name='Created At', default=timezone.now)
    updated_at = models.DateTimeField(verbose_name='Updated At', default=timezone.now)

    # def save(self, *args, **kwargs):
    #     ''' On save, update timestamps '''
    #     if not self.id:
    #         self.created_at = timezone.now()
    #     self.updated_at = timezone.now()
    #     return super(Question, self).save(*args, **kwargs)


class QuestionVote(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='question_votes')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='question_votes')
    vote = models.SmallIntegerField(verbose_name='Vote count')
    created_at = models.DateTimeField(verbose_name='Created At', default=timezone.now)
