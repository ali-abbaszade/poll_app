from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from polls import models

from . import serializers


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def question_list(request):
    questions = models.Question.objects.all()
    serializer = serializers.QuestionSerializer(questions, many=True)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def question_detail(request, pk):
    question = get_object_or_404(models.Question, pk=pk)
    serializer = serializers.QuestionSerializer(question)
    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def question_vote(request, pk):
    question = get_object_or_404(models.Question, pk=pk)
    choice = question.choices.get(choice_text=request.data["choice_text"])
    if request.user.id in question.voters:
        raise PermissionDenied("You have already submitter your vote for this question")
    choice.vote_count += 1
    question.voter.add(request.user)
    choice.save()
    serializer = serializers.QuestionSerializer(question)
    return Response(serializer.data)


@api_view(["POST"])
def signup_view(request):
    try:
        data = request.data
        user = User.objects.create(
            username=data.get("username"),
            email=data.get("email"),
            password=data.get("password"),
        )
        serializer = serializers.UserSerializer(user)
        return Response(serializer.data)
    except:
        content = {"detail": "User with this username already exists."}
        return Response(content, status.HTTP_400_BAD_REQUEST)
