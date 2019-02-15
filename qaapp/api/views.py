from rest_framework import viewsets, mixins
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from qaapp.api.custom_pagination import QuestionPagination
from qaapp.api.custom_permission import CustomIsAuthenticated
from .serializers import QuestionSerializer


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
    permission_classes = (CustomIsAuthenticated,) # can be IsAuthenticatedOrReadOnly also
