from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
# Create your models here.
class Book(models.Model):

    name = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    year_published = models.PositiveIntegerField()
    book_type = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name
    
    def max_loan_days(self):
        if self.book_type == 1:
            return 10
        elif self.book_type == 2:
            return 5
        elif self.book_type == 3:
            return 2
        return 0

    
class Customer( AbstractUser):
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    age = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name
        
    class Meta:
        verbose_name = "Customer"

class Loan(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="loans")
    loan_date = models.DateField()
    return_date = models.DateField(null=True,blank=True)
    is_return=models.BooleanField(default=False)
    def __str__(self):
        return f"Loan ID: {self.pk} - {self.customer.name} - {self.book.name}"