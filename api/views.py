from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth import authenticate
from .models import *
from .serializers import *


class UserCreate(CreateAPIView):
    authentication_classes = ()
    permission_classes = ()

    serializer_class = UserSerializer


class LoginView(APIView):
    permission_classes = ()

    def post(self, request, ):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)

        if user:
            return Response({"token": user.auth_token.key})
        else:
            return Response({"error": "Wrong Credentials"}, status=status.HTTP_400_BAD_REQUEST)


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

    check = Vote.check_vote(question_id, user_id, choice_id)
    if check:
        return Response({
            "message": "Siz ovoz bergansiz!"
        }, status=200)
    vote = Vote.poll_vote(question_id, user_id, choice_id)

    return Response({
        'id': vote.id,
        'question': vote.question.question_text,
        'author': vote.vote_author.username,
        'choice': vote.choice.choice_text,
        'created_date': vote.created_date
    }, status=201)
