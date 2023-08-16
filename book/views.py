# library/views.py
from collections import UserDict
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from .models import Book, Customer, Loan
from datetime import date, timedelta

################## ADD BOOK ########################################
def add_book(request):
    if request.method == 'POST':
        print(request.POST)
        name = request.POST.get('name')
        author = request.POST.get('author')
        year_published = int(request.POST.get('year_published'))
        book_type = int(request.POST.get('book_type'))
        book = Book.objects.create(name=name, author=author, year_published=year_published, book_type=book_type)
        
        book.save()
        return redirect('display_books')
    return render(request, 'add_book.html')
############## DISPLAY BOOK #########################################
def display_books(request):
    books = Book.objects.all()
    new_books=[]
    for book in books:
        
        new_books.append({"book": book,"loan":book.loans.filter(is_return=False)})
    print(new_books)
    return render(request, 'display_books.html', {'books': new_books})

def return_book(request,book_id):
    loan=Loan.objects.filter(book_id=book_id,is_return=False)[0]
    loan.return_date=date.today()
    loan.is_return=True
    loan.save()
    return redirect('display_books')
################### FIND BOOK ##########################
def find_book(request):
    results=[]
    search_query = request.GET.get('search')
    # if request.method == 'POST':
    if search_query:
        # query = request.POST['search_query']
        results = Book.objects.filter(name__icontains=search_query)
        return render(request, 'find_book.html', {'results': results, 'search_query': search_query})
    return render(request, 'index.html')
    #return render(request, 'find_book.html')
################ RMOVE BOOK ######################
def remove_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    book.delete()
    return redirect('display_books')
################# LOAN BOOK #############################
def loan_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        assert 'customer_id' in request.POST,"Missing 'customer_id' in POST "

        customer_id = int(request.POST['customer_id'])
        customer = get_object_or_404(Customer, id=customer_id)
        loan_date = date.today()
        
        loan = Loan.objects.create(customer=customer, book=book, loan_date=loan_date)
        return redirect('display_books')
    customers = Customer.objects.all()
    return render(request, 'loan_book.html', {'book': book, 'customers': customers})


#################### INDEX #################################
def index(request):
    print("index function entered !!!!!!!!!!!!")
    return render(request, "index.html")

################## LOGOUT ##############################
def logout_view(request):
    print("logout function entered !!!!!!!!!!!!")
    logout(request)
    print("rrrrrr")
    #return redirect('login')
    return render(request,'logout.html')
    
from django.contrib.auth.models import User

############### REGISTER ###################################
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

################## LOGIN ################################
def login_view(request):
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
            return redirect("index")
        else:
            print(f"!! error login. user is:{user_c}")
            # If authentication fails, show an error message or redirect back to the login page
            error_message = "Invalid credentials. Please try again."
            return render(request, "index.html", {"error_message": error_message})

    #return render("log_in_out.html")
    return render(request, 'log_in_out.html')



