from rest_framework.generics import ListAPIView

from qaapp.api.custom_pagination import QuestionPagination
from .serializers import QuestionSerializer


class QuestionListApiView(ListAPIView):
    serializer_class = QuestionSerializer
    model = serializer_class.Meta.model
    queryset = model.objects.all()
    pagination_class = QuestionPagination
