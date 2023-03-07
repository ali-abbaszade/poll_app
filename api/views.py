from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from polls import models

from . import serializers


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def question_list(request):
    questions = models.Question.objects.all()
    serializer = serializers.QuestionSerializer(questions, many=True)
    return Response(serializer.data)

    

