from rest_framework.generics import ListAPIView
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import *
from .serializers import *


# Create your views here.
class Polls(ListAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class Choice(ListAPIView):
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer


@api_view(['POST'])
def vote_views(request):
    question_id = request.data.get('question_id')
    user_id = request.user.id
    choice_id = request.data.get('choice_id')

    vote = Vote.poll_vote(question_id, user_id, choice_id)

    return Response({
        'id': vote.id,
        'question': vote.question.question_text,
        'author': vote.vote_author.username,
        'choice': vote.choice.choice_text,
        'created_date': vote.created_date
    })
