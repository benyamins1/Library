# library/views.py
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from .models import Book, Customer, Loan
from datetime import date, timedelta


def add_book(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        author = request.POST.get('author')
        year_published = int(request.POST.get('year_published'))
        book_type = int(request.POST.get('book_type'))
        book = Book.objects.create(name=name, author=author, year_published=year_published, book_type=book_type)
        #book = Book.objects.create(name, author, year_published, book_type)
        book.save()
        return redirect('display_books')
    return render(request, 'add_book.html')

def display_books(request):
    books = Book.objects.all()
    return render(request, 'display_books.html', {'books': books})

def find_book(request):
    if request.method == 'POST':
        query = request.POST['search_query']
        books = Book.objects.filter(name__icontains=query)
        return render(request, 'display_books.html', {'books': books})
    return render(request, 'find_book.html')

def remove_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    book.delete()
    return redirect('display_books')

def loan_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        customer_id = int(request.POST['customer_id'])
        customer = get_object_or_404(Customer, id=customer_id)
        loan_date = date.today()
        return_date = loan_date + timedelta(days=book.max_loan_days())
        loan = Loan.objects.create(customer=customer, book=book, loan_date=loan_date, return_date=return_date)
        return redirect('display_books')
    customers = Customer.objects.all()
    return render(request, 'loan_book.html', {'book': book, 'customers': customers})





def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to a home page or other view
       
            # Display an error message

    else: 
        render(request, 'login.html')

def logout_view(request):
    logout(request)
    return render(request, 'logout.html')

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create a corresponding Customer object with city and age fields
            # and associate it with the new user
            return redirect('login')  # Redirect to the login page

        else:
            form = UserCreationForm()

    return render(request, 'register.html', {'form': form})


