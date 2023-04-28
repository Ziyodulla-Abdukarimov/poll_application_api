from rest_framework import serializers
from model.models import Choice, Question


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer

    class Meta:
        model = Question
        fields = ['id', 'question_text', 'creator', 'creator_type', 'choice_type', 'choices']

    def get_choices(self, question):
        queryset = Choice.objects.filter(question_id=question.id)
        serializer = ChoiceSerializer(queryset, many=True)
        return serializer.data
