from django import forms 
from .models import Question


class PracticeSetupForm(forms.Form):
    """Define a form class for practice set up."""
    subject = forms.ChoiceField(
        choices=[("", "Select a Subject") ,*Question.SUBJECT_CHOICES],
        widget=forms.Select(attrs={
            "class": "form-select",
            "id": "id_subject",
            }),
        required=True,
        label="Subject"
    )

    domain = forms.ChoiceField(
        choices=[("", "Select a Domain"), *Question.DOMAIN_CHOICES],
        widget=forms.Select(attrs={
            "class": "form-select",
            "id": "id_domain",
            }),
        required=True,
        label="Domain"
    )

    skill = forms.ChoiceField(
        choices=[("", "Select a difficulty"), *Question.SKILL_CHOICES],
        widget=forms.Select(attrs={"class": "form-select"}),
        required=True,
        label="Difficulty"
    )

    num_questions = forms.IntegerField(
        min_value=1,
        max_value=40,
        widget=forms.NumberInput(attrs={"class": "form-control"}),
        required=True,
        label="Number of Questions"
    )

    timer = forms.IntegerField(
        min_value=1,
        max_value=120,
        widget=forms.NumberInput(attrs={
            "class": "form-control",
        }),
        required=True,
        label="Timer Minute"
    )