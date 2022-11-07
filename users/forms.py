from django.contrib.auth.forms import UserCreationForm

class CustomUserCreationFrom(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ("email",)