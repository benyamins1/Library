# library/urls.py
from django.urls import path
from book import views, views_old

urlpatterns = [
    path("", views.index, name="index"),
    path('find_book/', views_old.find_book, name='find_book'),
    path('remove_book/<int:book_id>/', views_old.remove_book, name='remove_book'),
    path('loan_book/<int:book_id>/', views_old.loan_book, name='loan_book'),
    path('add_book/', views_old.add_book, name='add_book'),
    path('display_books/', views_old.display_books, name='display_books'),
    path('login/', views_old.login, name='login'),
    path('logout/', views_old.logout, name='logout'),
    path('register/', views_old.register, name='register'),
]
