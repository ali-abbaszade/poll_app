from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)


class Question(models.Model):
    voter = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)
    question_title = models.CharField(max_length=255)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_date",)

    @property
    def voters(self):
        voters = self.voter.values_list("id", flat=True)
        return voters

    def __str__(self):
        return self.question_title


class Choice(models.Model):
    question = models.ForeignKey(
        "Question", related_name="choices", on_delete=models.CASCADE
    )
    choice_text = models.CharField(max_length=255)
    vote_count = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
