from django import forms

from .models import (
    Quiz,
    Question,
    Answer,
    Comment
)

class QuizForm(forms.ModelForm):

    class Meta:

        model = Quiz

        fields = [
            "title",
            "description",
            "image",
            "category"
        ]

class QuestionForm(forms.ModelForm):

    class Meta:

        model = Question

        fields = [
            "text"
        ]

class AnswerForm(forms.ModelForm):

    class Meta:

        model = Answer

        fields = [
            "text",
            "is_correct"
        ]


class CommentForm(forms.ModelForm):

    class Meta:

        model = Comment

        fields = [
            "text"
        ]

        widgets = {

            "text": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Напишите комментарий..."
                }
            )

        }