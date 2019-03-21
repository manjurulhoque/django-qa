from django.db.models import Prefetch, Sum
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework_simplejwt.models import TokenUser

from qaapp.api.custom_pagination import QuestionPagination
from qaapp.api.custom_permission import CustomIsAuthenticated, IsAuthenticatedForQuestionFavorite
from qaapp.models import Question, QuestionVote, Answer, Favorite
from .serializers import QuestionSerializer, QuestionFavoriteSerializer


class QuestionListApiView(ListAPIView):
    serializer_class = QuestionSerializer
    model = serializer_class.Meta.model
    queryset = model.objects.all().order_by('id')
    pagination_class = QuestionPagination


# To disable getting all questions by this viewSet, remove ListModelMixin
class QuestionViewSet(mixins.CreateModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    serializer_class = QuestionSerializer
    queryset = serializer_class.Meta.model.objects.all()
    permission_classes = (CustomIsAuthenticated,)  # can be IsAuthenticatedOrReadOnly also

    def create(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({'message': 'Unauthenticated'}, status.HTTP_400_BAD_REQUEST)
        # print(TokenUser.objects.get(key=request.user.token))
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        # Perform the lookup filtering.
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        # print(self.kwargs)
        obj = get_object_or_404(queryset, **filter_kwargs)
        # May raise a permission denied
        self.check_object_permissions(self.request, obj)

        return obj

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        data['votes_count'] = instance.question_votes.aggregate(Sum('vote'))['vote__sum']
        data['favorites_count'] = instance.question_favorites.count()
        return Response(data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.user != request.user:
            return Response({'message': 'Unauthorized'}, status.HTTP_401_UNAUTHORIZED)

        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if not instance:
            return Response({}, status.HTTP_404_NOT_FOUND)
        if instance.user.id == request.user.id:
            self.perform_destroy(instance)
            return Response({}, status.HTTP_204_NO_CONTENT)
        else:
            return Response({'message': 'Unauthorized'}, status.HTTP_401_UNAUTHORIZED)

    def perform_destroy(self, instance):
        instance.delete()


@api_view(['POST'])
@csrf_exempt
def question_vote(request, question_id=None, flag='upvote'):
    # print(flag, question_id)
    # return redirect(reverse_lazy('qa:home'))
    question = Question.objects.get(id=question_id)
    if request.method == 'POST':
        if QuestionVote.objects.filter(user=request.user, question=question).exists():  # check if exists
            vote = QuestionVote.objects.get(user=request.user, question=question)
            if vote.vote == -1 and flag == 'upvote':  # if down vote and request for upvote
                vote.vote = 1
                vote.save()
                return Response({'status': True, 'message': 'upvoted'}, status.HTTP_200_OK)
            elif vote.vote == 1 and flag == 'upvote':  # if already given upvote and want to remove the upvote
                vote.delete()
                return Response({'status': True, 'message': 'upvote removeed'}, status.HTTP_200_OK)
            elif vote.vote == -1 and flag == 'downvote':  # if already given downvote and want to remove the downvote
                vote.delete()
                return Response({'status': True, 'message': 'downvote removed'}, status.HTTP_200_OK)
            else:  # if already downvote and want to upvote
                vote.vote = 1
                vote.save()
            return Response({'status': True, 'message': 'upvoted'}, status.HTTP_200_OK)
        else:
            vote = QuestionVote()
            vote.user = request.user
            vote.question = question
            if flag == 'upvote':
                vote.vote = 1
                vote.save()
                return Response({'status': True, 'message': 'upvoted'}, status.HTTP_200_OK)
            else:
                vote.vote = -1
                vote.save()
                return Response({'status': True, 'message': 'dowvoted'}, status.HTTP_200_OK)
    else:
        return Response({'message': 'Unauthorized'}, status.HTTP_401_UNAUTHORIZED)


class QuestionFavoriteViewSet(mixins.CreateModelMixin,
                              mixins.DestroyModelMixin,
                              viewsets.GenericViewSet):
    serializer_class = QuestionFavoriteSerializer
    queryset = serializer_class.Meta.model.objects.all()
    # permission_classes = (IsAuthenticatedForQuestionFavorite,)

    """
       Create a model instance
    """

    def create(self, request, *args, **kwargs):
        question = Question.objects.get(id=kwargs.pop('question_id'))
        if self.get_queryset().filter(question_id=question.id, user_id=request.user.id).exists():
            return Response({'status': False, 'message': 'already favourited'}, status=status.HTTP_201_CREATED)
        serializer = self.get_serializer(data={'question': question.id, 'user': self.request.user.id})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()

    """
        Destroy a model instance.
    """

    def destroy(self, request, *args, **kwargs):
        instance = Question.objects.get(id=kwargs.pop('question_id'))
        if not instance:
            return Response({'status': False, 'message': 'Invalid'}, status=status.HTTP_201_CREATED)
        self.perform_destroy(instance)
        return Response({'status': True, 'message': 'unfavorited'}, status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()


@api_view(['GET'])
def check_user_vote(request, question_id=None):
    question = Question.objects.get(id=question_id)
    if not question:
        return JsonResponse({'status': False, 'message': 'Question not found'})

    context = {}
    if request.user.is_authenticated:
        vote = request.user.question_votes.filter(question_id=question_id).first()
        if Favorite.objects.filter(user_id=request.user.id, question_id=question.id).exists():
            context['favorited'] = True
        else:
            context['favorited'] = False

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
    return JsonResponse({'status': True, 'context': context})
