# library/urls.py
from django.urls import path
from book import views

urlpatterns = [
    path("", views.index, name="index"),
    path('find_book/', views.find_book, name='find_book'),
    path('remove_book/<int:book_id>/', views.remove_book, name='remove_book'),
    path('loan_book/<int:book_id>/', views.loan_book, name='loan_book'),
    path('add_book/', views.add_book, name='add_book'),
    path('display_books/', views.display_books, name='display_books'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('return_book/<int:book_id>/', views.return_book, name='return_book'),
]
