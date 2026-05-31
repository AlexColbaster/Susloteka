from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group, User

from .models import Film, Review


class FilmForm(forms.ModelForm):
    class Meta:
        model = Film
        fields = ['title', 'description', 'video', 'genres']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Название фильма'}),
            'description': forms.Textarea(attrs={'rows': 6, 'placeholder': 'Краткое описание фильма'}),
            'video': forms.ClearableFileInput(),
            'genres': forms.CheckboxSelectMultiple(),
        }


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'text']
        widgets = {
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 10}),
            'text': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Ваш отзыв'}),
        }


class RegistrationForm(UserCreationForm):
    ROLE_CHOICES = [
        ('client', 'Клиент'),
        ('librarian', 'Библиотекарь'),
    ]

    role = forms.ChoiceField(choices=ROLE_CHOICES, widget=forms.RadioSelect)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Логин'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['role'].initial = 'client'

    def save(self, commit=True):
        user = super().save(commit=commit)
        role = self.cleaned_data['role']
        group, _ = Group.objects.get_or_create(name=role)
        user.groups.clear()
        user.groups.add(group)
        return user
