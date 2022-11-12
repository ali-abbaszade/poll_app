from django.db import models
from django.contrib.auth.models import User

class Question(models.Model):
    voter = models.ManyToManyField(User, blank=True)
    question_title = models.CharField(max_length=255)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_date',)

    @property
    def voters(self):
        voters = self.voter.values_list('id', flat=True)
        return voters      

    def __str__(self):
        return self.question_title

class Choice(models.Model):
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=255)
    vote_count = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text