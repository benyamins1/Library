# library/views.py
from collections import UserDict
from pyexpat.errors import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
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
    customers = UserDict.objects.all()
    return render(request, 'loan_book.html', {'book': book, 'customers': customers})



def index(request):
    print("index function entered !!!!!!!!!!!!")
    return render(request, "index.html")


def logout(request):
    print("logout function entered !!!!!!!!!!!!")
    logout(request)
    #return redirect("index")
    return render(request, 'logout.html')


# def register(request):
#     print("--- login function entered ---")
#     try:
#         if request.method == "POST":
#             username = request.POST.get("username")
#             password = request.POST.get("password")
#             print(f"username={username}. passowrd={password}")
            
#             user_c = Customer.objects.create_user(username, "", password)
#             user_c.save()
        
#     except Exception as e:
#         messages.error(request, f"Error occured on registration {e}.")
#     messages.success(request, f"User Registered Successfuly.")
#     return redirect("index")
from django.contrib.auth.models import User

def register(request):
    print("--- register function entered ---")
    try:
        if request.method == "POST":
            username = request.POST.get("username")
            password = request.POST.get("password")
            print(f"username={username}. password={password}")
            
            if Customer.objects.filter(username=username).exists():
                messages.error(request, "Username already exists.")
            else:
                user_c = Customer.objects.create_user(username, "", password)
                user_c.save()
                messages.success(request, "User Registered Successfully.")
        return redirect("index")
    except Exception as e:
        messages.error(request, f"Error occurred on registration: {e}")
        return redirect("index")


def login(request):
    print("login function entered !!!!!!!!!!!!")
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        print(f"username={username}. passowrd={password}")

        # Authenticate the user - validating user password. return user object if valid
        user_c = authenticate(request, username=username, password=password)
        print(f"authenticate passed. user is:{user_c}")

        if user_c is not None:
            # If the credentials are correct, log in the user
            login(request, user_c)
            print(f"** login passed. user is:{user_c}")
            return redirect("playlist")
        else:
            print(f"!! error login. user is:{user_c}")
            # If authentication fails, show an error message or redirect back to the login page
            error_message = "Invalid credentials. Please try again."
            return render(request, "index.html", {"error_message": error_message})

    return redirect("index")



