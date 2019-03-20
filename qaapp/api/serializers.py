from rest_framework import serializers

from accounts.api.serializers import UserSerializer
from qaapp.models import Question, Favorite, Answer


class QuestionFavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = "__all__"


class AnswerSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Answer
        fields = "__all__"


class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, read_only=True)
    user = UserSerializer(read_only=True)  # read only mean

    class Meta:
        model = Question
        fields = "__all__"
        # read_only_fields = ("user", "answers")
