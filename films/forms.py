from django import forms

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
        fields = ['author', 'rating', 'text']
        widgets = {
            'author': forms.TextInput(attrs={'placeholder': 'Ваше имя'}),
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 10}),
            'text': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Ваш отзыв'}),
        }
