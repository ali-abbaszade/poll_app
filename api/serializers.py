from rest_framework import serializers

from polls import models


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        extra_kwargs = {
            'vote_count': {'read_only': True}
        }
        model = models.Choice
        fields = ['choice_text', 'vote_count']


class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True)

    class Meta:
        model = models.Question
        fields = ['id', 'question_title', 'choices', 'created_date']
