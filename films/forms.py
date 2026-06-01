from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group, User

from .models import Director, Film, Review


class FilmForm(forms.ModelForm):
    director_names = forms.CharField(
        label='Режиссёры',
        required=False,
        widget=forms.HiddenInput(),
    )

    class Meta:
        model = Film
        fields = ['title', 'description', 'video', 'genres']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Название фильма'}),
            'description': forms.Textarea(attrs={'rows': 6, 'placeholder': 'Краткое описание фильма'}),
            'video': forms.ClearableFileInput(),
            'genres': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.directors = Director.objects.order_by('name')

    def clean_director_names(self):
        raw_value = self.cleaned_data.get('director_names', '').strip()
        if not raw_value:
            return []

        names = [part.strip() for part in raw_value.split(',') if part.strip()]
        if not names:
            return []

        directors = []
        missing = []
        for name in names:
            director = Director.objects.filter(name__iexact=name).first()
            if director is None:
                missing.append(name)
            elif director not in directors:
                directors.append(director)

        if missing:
            raise forms.ValidationError(f"Не найдены режиссёры: {', '.join(missing)}")

        return directors

    def save(self, commit=True):
        film = super().save(commit=False)
        if commit:
            film.save()
            self.save_m2m()
            film.directors.set(self.cleaned_data.get('director_names', []))
        return film


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'text']
        widgets = {
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 10}),
            'text': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Ваш отзыв'}),
        }


class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Логин'}),
        }

    def save(self, commit=True):
        user = super().save(commit=commit)
        if commit:
            group, _ = Group.objects.get_or_create(name='client')
            user.groups.add(group)
        return user
