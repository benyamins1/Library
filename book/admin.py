from django.contrib import admin
from book.models import Book,Customer,Loan
from django.contrib.auth.admin import UserAdmin
#from .models import User

admin.site.register(Customer, UserAdmin)

# Register your models here.
admin.site.register(Book)
#admin.site.register(Customer)
admin.site.register(Loan)