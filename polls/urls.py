from django.urls import path
from . import views

app_name = "polls"

urlpatterns = [
    path('', views.index_view, name="index"),
    path('polls/', views.poll_list, name="poll-list"),
    path('vote/<int:pk>/', views.vote_view, name="vote"),
    path('result/<int:pk>/', views.result_view, name='result')
]