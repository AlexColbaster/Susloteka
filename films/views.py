from django.db.models import Avg, Count
from django.shortcuts import get_object_or_404, redirect, render

from .forms import FilmForm, ReviewForm
from .models import Film


def film_list(request):
    query = request.GET.get('q', '').strip()
    films = Film.objects.prefetch_related('genres', 'reviews')
    if query:
        films = films.filter(title__icontains=query)
    films = films.annotate(avg_rating=Avg('reviews__rating'), reviews_total=Count('reviews'))
    return render(request, 'films/film_list.html', {'films': films, 'query': query})


def film_detail(request, pk):
    film = get_object_or_404(Film.objects.prefetch_related('genres', 'reviews'), pk=pk)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.film = film
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
        },
    )


def film_create(request):
    if request.method == 'POST':
        form = FilmForm(request.POST, request.FILES)
        if form.is_valid():
            film = form.save()
            return redirect('film_detail', pk=film.pk)
    else:
        form = FilmForm()

    return render(request, 'films/film_form.html', {'form': form})
