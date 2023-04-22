from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView, CreateAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from .serializers import *
from model.models import *


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
    permission_classes = [AllowAny]
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class Choice(ListAPIView):
    permission_classes = [AllowAny]
    queryset = Choice.objects.all()
    serializer_class = OneChoiceSerializer


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def vote_views(request):
    question_id = request.data.get('question_id')
    user_id = request.user.id
    question = get_object_or_404(Question, id=question_id)
    if question.choice_type == 'one':
        choice_id = request.data.get('choice')
        check = OneChoice.check_vote(question_id, user_id)
        if check:
            return Response({
                "message": "Siz ovoz bergansiz!"
            }, status=200)
        vote = OneChoice.poll_vote(question_id, user_id, choice_id)
        return Response({
            'id': vote.id,
            'question': vote.question.question_text,
            'author': vote.vote_author.username,
            'choice': vote.choice.choice_text,
            'created_date': vote.created_date
        }, status=201)

    elif question.choice_type == 'multi':
        selected_choices = request.data.get('choice', [])
        check = MultiChoice.check_vote(question_id, user_id)
        if check:
            return Response({
                "message": "Siz ovoz bergansiz!"
            }, status=200)
        if not selected_choices:
            raise ValidationError('Siz hechnima belgilamadingiz!')
        selected_choice_ids = [choice['id'] for choice in selected_choices]
        vote = MultiChoice.poll_vote(question_id, user_id, selected_choice_ids)
        return Response({
            'id': vote.id,
            'question': vote.question.question_text,
            'author': vote.vote_author.username,
            'choice': [choice.choice_text for choice in vote.choice.all()],
            'created_date': vote.created_date
        }, status=201)
