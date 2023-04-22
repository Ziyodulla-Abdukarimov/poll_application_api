from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Question(models.Model):
    question_text = models.CharField(max_length=200)

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text


class Vote(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    vote_author = models.ForeignKey(User, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question.question_text + " " + self.vote_author.last_name

    @staticmethod
    def check_vote(question_id, user_id, choice_id):
        if Vote.objects.filter(question=question_id, vote_author=user_id, choice=choice_id).exists():
            return True

    @staticmethod
    def poll_vote(question_id, user_id, choice_id):
        choice = Choice.objects.get(id=choice_id)
        vote = Vote(
            question=Question.objects.get(id=question_id),
            vote_author=User.objects.get(id=user_id),
            choice=choice
        )
        vote.save()
        choice.votes += 1
        choice.save()
        return vote
