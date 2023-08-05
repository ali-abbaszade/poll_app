from django.contrib.auth.forms import UserCreationForm
from polls import models


class CustomUserCreationFrom(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = models.CustomUser
        fields = UserCreationForm.Meta.fields + ("email",)
