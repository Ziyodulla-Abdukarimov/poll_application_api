from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import QuestionS, MyQuestions

router = DefaultRouter()
router.register('question', QuestionS, basename='clientQuestion')
router.register('my-questions', MyQuestions, basename='my_questions')

urlpatterns = [
    path('', include(router.urls)),
]
