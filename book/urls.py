# library/urls.py
from django.urls import path
from book import views, views_old

urlpatterns = [
    path("", views.index, name="index"),
    path('find_book/', views.find_book, name='find_book'),
    path('remove_book/<int:book_id>/', views.remove_book, name='remove_book'),
    path('loan_book/<int:book_id>/', views.loan_book, name='loan_book'),
    path('add_book/', views.add_book, name='add_book'),
    path('display_books/', views.display_books, name='display_books'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.register, name='register'),
]
