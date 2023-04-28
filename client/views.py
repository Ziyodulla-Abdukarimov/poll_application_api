from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from model.models import Question
from .serializer import QuestionSerializer


# Create your views here.
# start User create poll
class QuestionS(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = QuestionSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = Question.objects.filter(creator=user)
        return queryset


class MyQuestions(ModelViewSet):
    serializer_class = QuestionSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = Question.objects.filter(creator=user)
        return queryset
