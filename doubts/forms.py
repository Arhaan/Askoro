from django import forms
from .models import Answer, Question


class QuestionCreationForm(forms.ModelForm):

    class Meta:
        model = Question
        fields = ['title', 'text', 'subject']


class QuestionUpdateForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'text', 'subject']


class AnswerCreationForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['text']


class AnswerUpdateForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['text']
