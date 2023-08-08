import pytest
from pytest_django.asserts import assertTemplateUsed, assertContains, assertRedirects
from django.contrib.auth import get_user_model
from django.urls import reverse
from polls import models

pytestmark = pytest.mark.django_db


def test_home_page_returns_correct_response(client):
    response = client.get(reverse("polls:index"))
    assert response.status_code == 200
    assertTemplateUsed(response, "polls/index.html")


def test_question_model_exits(client):
    User = get_user_model()
    question = models.Question.objects.create(question_title="Test Title")
    voter = User.objects.create(username="testuser", password="testpassword")
    question.voter.add(voter)

    questions_count = models.Question.objects.count()
    assert questions_count == 1
    assert str(question) == "Test Title"


def test_result_page_returns_correct_response(client):
    User = get_user_model()
    question = models.Question.objects.create(question_title="Test Title")
    voter = User.objects.create(username="testuser", password="testpassword")
    question.voter.add(voter)
    choice = models.Choice.objects.create(question=question, choice_text="Test choice")

    client.force_login(voter)
    response = client.get(reverse("polls:result", args=[question.id]))
    assert response.status_code == 200
    assertTemplateUsed(response, "polls/result.html")
    assertContains(response, question.question_title)
    assertContains(response, choice.choice_text)


def test_vote_page_form_rendering(client):
    User = get_user_model()
    question = models.Question.objects.create(question_title="Test Title")
    voter = User.objects.create(username="testuser", password="testpassword")

    client.force_login(voter)
    response = client.get(reverse("polls:vote", args=[question.id]))
    assertContains(response, "<form ")
    assertContains(response, "csrfmiddlewaretoken")


def test_invalid_valid_vote_page_form_rendering(client):
    User = get_user_model()
    question = models.Question.objects.create(question_title="Test Title")
    voter = User.objects.create(username="testuser", password="testpassword")
    choice_1 = models.Choice.objects.create(question=question, choice_text="")

    client.force_login(voter)
    response = client.post(
        path=reverse("polls:vote", args=[question.id]),
        data={"choice": choice_1},
    )
    messages = list(response.context["messages"])
    assert len(messages) == 1
    assert str(messages[0]) == "You didn't select a choice!"


def test_valid_vote_page_form_rendering(client):
    User = get_user_model()
    question = models.Question.objects.create(question_title="Test Title")
    voter = User.objects.create(username="testuser", password="testpassword")
    choice_1 = models.Choice.objects.create(question=question, choice_text="choice_1")

    client.force_login(voter)
    response = client.post(
        path=reverse("polls:vote", args=[question.id]),
        data={"choice": choice_1.id},
    )

    assertRedirects(response, expected_url=reverse("polls:result", args=[question.id]))
    assert question.choices.first().vote_count == 1
