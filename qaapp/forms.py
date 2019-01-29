from django import forms
from django.forms import Textarea
from django.template.defaultfilters import slugify

from qaapp.models import Question, Answer


class QuestionCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.user = kwargs.pop('user')
        self.fields['title'].widget.attrs.update({'placeholder': 'Question title'})
        self.fields['body'].widget.attrs.update({'placeholder': 'Explain your question'})
        # self.fields['title'].label = 'Rule Title'

        self.fields["title"].error_messages = {
            "max_length": "This title is too long.",
            "required": "The title field is required."
        }
        self.fields["body"].error_messages = {
            "max_length": "This title is too long.",
            "required": "The body field is required.",
        }

    class Meta:
        model = Question
        fields = ("title", "body",)
        widgets = {
            'body': Textarea(attrs={'cols': 45, 'rows': 5, 'class': 'form-control'}),
        }
        labels = {
            "title": "Question Title",
            "body": "Explain your question",
        }

    def save(self, commit=True):
        question = super(QuestionCreateForm, self).save(commit=False)
        question.slug = slugify(self.cleaned_data['title'])
        if commit:
            question.save()
        return question


class AnswerCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["body"].widget = Textarea(attrs={'cols': 45, 'rows': 5, 'class': 'form-control'})
        self.fields["body"].widget.attrs.update({'placeholder': 'Give proper answer'})

    class Meta:
        model = Answer
        fields = ("body",)
