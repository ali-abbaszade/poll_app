from django.contrib import admin
from .models import Question, Choice, CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    pass


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 4


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    search_fields = ["question_title__icontains"]
    inlines = [ChoiceInline]
