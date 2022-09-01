from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import Author, Comment


class AuthorCreationForm(UserCreationForm):

    class Meta:
        model = Author
        fields = ("username", "email", "profile_photo", "description", "password1", "password2")


class AuthorChangeForm(UserChangeForm):

    class Meta:
        model = Author
        fields = ("username", "email", "profile_photo", "description")


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False,
                               widget=forms.Textarea)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'body']


class ContactForm(forms.Form):
    name = forms.CharField(label='Имя', max_length=30)
    email = forms.EmailField(label='Email', max_length=30)
    message = forms.CharField(label='Сообщение', max_length=300)
