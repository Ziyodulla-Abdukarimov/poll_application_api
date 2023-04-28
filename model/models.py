from django.contrib.auth.models import User
from django.db import models

ONE_CHOICE, MULTI_CHOICE = (
    'one',
    'multi'
)
ADMIN, CLIENT = (
    'admin',
    'client'
)


# Create your models here.
class Question(models.Model):
    question_text = models.CharField(max_length=200)

    CREATOR_TYPE = (
        (ADMIN, ADMIN),
        (CLIENT, CLIENT)
    )

    CHOICE_TYPE = (
        (ONE_CHOICE, ONE_CHOICE),
        (MULTI_CHOICE, MULTI_CHOICE)
    )
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    creator_type = models.CharField(choices=CREATOR_TYPE, max_length=100)
    choice_type = models.CharField(choices=CHOICE_TYPE, max_length=15)

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text


class OneChoice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    vote_author = models.ForeignKey(User, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question.question_text + " " + self.vote_author.last_name

    @staticmethod
    def check_vote(question_id, user_id):
        if OneChoice.objects.filter(question=question_id, vote_author=user_id).exists():
            return True

    @staticmethod
    def poll_vote(question_id, user_id, choice_id):
        choice = Choice.objects.get(id=choice_id)
        vote = OneChoice(
            question=Question.objects.get(id=question_id),
            vote_author=User.objects.get(id=user_id),
            choice=choice
        )
        vote.save()
        choice.votes += 1
        choice.save()
        return vote


class MultiChoice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    vote_author = models.ForeignKey(User, on_delete=models.CASCADE)
    choice = models.ManyToManyField(Choice)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question.question_text + " " + self.vote_author.last_name

    @staticmethod
    def check_vote(question_id, user_id):
        if MultiChoice.objects.filter(question=question_id, vote_author=user_id).exists():
            return True

    @staticmethod
    def poll_vote(question_id, user_id, choice):
        vote = MultiChoice(
            question=Question.objects.get(id=question_id),
            vote_author=User.objects.get(id=user_id)
        )
        vote.save()
        for choice_id in choice:
            choice = Choice.objects.get(id=choice_id)
            vote.choice.add(choice)
            choice.votes += 1
            choice.save()
        return vote
