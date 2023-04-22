from django.urls import path
from .views import *

urlpatterns = [
    path('vote/', vote_views, name='vote'),
    path('polls/', Polls.as_view(), name='polls'),
    path('choice/', Choice.as_view(), name='choice'),
]
