# library/views.py
from datetime import date

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from .models import Book, Customer, Loan


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
    new_books = []
    for book in books:
        new_books.append({"book": book, "loan": book.loans.filter(is_return=False)})
    print(new_books)
    return render(request, 'display_books.html', {'books': new_books})


def return_book(request, book_id):
    loan = Loan.objects.filter(book_id=book_id, is_return=False)[0]
    loan.return_date = date.today()
    loan.is_return = True
    loan.save()
    return redirect('display_books')


################### FIND BOOK ##########################

def find_book(request):
    query = request.GET.get('query', '')  # Get the search query from the URL parameter
    books = Book.objects.filter(name__icontains=query)

    context = {
        'books': books,
        'query': query,
    }

    return render(request, 'find_book.html', context)


################ RMOVE BOOK ######################



def remove_book(request, book_id = 4):

    if request.method == 'POST' and request.POST['book_id']:
        book_id = request.POST['book_id']
        book = Book.objects.filter(id=book_id)
        book.delete()
        return redirect('find_book')  # Redirect to a page displaying the list of books

    else:
        book = Book.objects.filter(id=book_id)

    context = {
        'book': book,
    }
    return render(request, 'remove.html', context)


################# LOAN BOOK #############################
def loan_book(request, book_id):

    book = Book.objects.filter(id=book_id).get()
    if not book:
        return HttpResponse("Book not found.")

    if request.method == 'POST':
        assert 'customer_id' in request.POST, "Missing 'customer_id' in POST "

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
    query = request.GET.get('q')
    books = []
    if query:
        books = Book.objects.filter(name__contains=query)

    # if request.method=="GET":
    return render(request, "index.html", {'books': books})


################## LOGOUT ##############################
def logout_view(request):
    print("logout function entered !!!!!!!!!!!!")
    logout(request)
    print("rrrrrr")
    # return redirect('login')
    return render(request, 'logout.html')


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

    # return render("log_in_out.html")
    return render(request, 'log_in_out.html')
