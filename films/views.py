from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from functools import wraps
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Avg, Count
from django.http import Http404

from .forms import FilmForm, RegistrationForm, ReviewForm
from .models import Film, Review
from .xlsx_export import export_model_to_xlsx


def is_librarian(user):
    return user.is_authenticated and (user.is_superuser or user.groups.filter(name='librarian').exists())


def is_client(user):
    return user.is_authenticated and user.groups.filter(name='client').exists()


def librarian_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(f'/accounts/login/?next={request.path}')
        if not is_librarian(request.user):
            messages.error(request, 'Недостаточно прав.')
            return redirect('film_list')
        return view_func(request, *args, **kwargs)

    return wrapper


def film_list(request):
    query = request.GET.get('q', '').strip()
    films = Film.objects.prefetch_related('directors', 'genres', 'reviews')
    if query:
        films = films.filter(title__icontains=query)
    films = films.annotate(avg_rating=Avg('reviews__rating'), reviews_total=Count('reviews'))
    return render(request, 'films/film_list.html', {'films': films, 'query': query})


def register_view(request):
    if request.user.is_authenticated:
        return redirect('film_list')

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Аккаунт создан.')
            return redirect('film_list')
    else:
        form = RegistrationForm()

    return render(request, 'registration/register.html', {'form': form})


def film_detail(request, pk):
    film = get_object_or_404(Film.objects.prefetch_related('directors', 'genres', 'reviews__user'), pk=pk)
    user_review = None
    reviews = list(film.reviews.select_related('user').all())

    if request.user.is_authenticated:
        for review in reviews:
            if review.user_id == request.user.id:
                user_review = review
                break
        reviews.sort(key=lambda review: (review.user_id != request.user.id, -review.created_at.timestamp()))
    else:
        reviews.sort(key=lambda review: -review.created_at.timestamp())

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect(f'/accounts/login/?next=/film/{film.pk}/')
        form = ReviewForm(request.POST)
        if form.is_valid():
            if user_review is not None:
                form.add_error(None, 'У вас уже есть отзыв к этому фильму. Сначала удалите старый.')
            else:
                review = form.save(commit=False)
                review.film = film
                review.user = request.user
                review.author = request.user.username
                review.save()
                return redirect('film_detail', pk=film.pk)
    else:
        form = ReviewForm()

    return render(
        request,
        'films/film_detail.html',
        {
            'film': film,
            'review_form': form,
            'reviews': reviews,
            'user_review': user_review,
            'can_moderate_reviews': is_librarian(request.user),
            'can_review': request.user.is_authenticated and user_review is None,
        },
    )


@librarian_required
def film_create(request):
    if request.method == 'POST':
        form = FilmForm(request.POST, request.FILES)
        if form.is_valid():
            film = form.save()
            return redirect('film_detail', pk=film.pk)
    else:
        form = FilmForm()

    return render(request, 'films/film_form.html', {'form': form, 'directors': form.directors})


@login_required
def review_delete(request, pk):
    review = get_object_or_404(Review, pk=pk)
    film_pk = review.film_id
    if request.method == 'POST':
        if request.user.is_authenticated and (is_librarian(request.user) or review.user_id == request.user.id):
            review.delete()
            messages.success(request, 'Отзыв удалён.')
        else:
            messages.error(request, 'Недостаточно прав.')
    return redirect('film_detail', pk=film_pk)


@login_required
def export_table(request, table_name):
    allowed = {
        'films': ('films', 'Film'),
        'directors': ('films', 'Director'),
        'genres': ('films', 'Genre'),
        'reviews': ('films', 'Review'),
        'logs': ('films', 'Log'),
    }
    if table_name not in allowed:
        raise Http404('Таблица не найдена')
    app_label, model_name = allowed[table_name]
    return export_model_to_xlsx(app_label, model_name)
