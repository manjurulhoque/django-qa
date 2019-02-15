from rest_framework import viewsets, mixins, status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework_simplejwt.models import TokenUser

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
