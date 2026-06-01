from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('', views.film_list, name='film_list'),
    path('add/', views.film_create, name='film_create'),
    path('film/<int:pk>/', views.film_detail, name='film_detail'),
    path('review/<int:pk>/delete/', views.review_delete, name='review_delete'),
    path('export/<str:table_name>/', views.export_table, name='export_table'),
    path('register/', views.register_view, name='register'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
]
