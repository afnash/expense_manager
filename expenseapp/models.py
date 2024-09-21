from django.db import models
from django.utils import timezone

# Base Expense model
class Expense(models.Model):
    CATEGORY_CHOICES = [
        ('FOOD', 'Food'),
        ('GROCERY', 'Grocery/Stationary'),
        ('BILLS', 'Bills'),
        ('OTHER', 'Other'),
    ]
    
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.category}: {self.description} - {self.amount}"

# Food model (optional if you want separate models)
class FoodExpense(models.Model):
    description = models.TextField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"Food: {self.description} - {self.amount}"

# Grocery/Stationary model
class GroceryStationaryExpense(models.Model):
    description = models.TextField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"Grocery/Stationary: {self.description} - {self.amount}"

# Bills model
class BillsExpense(models.Model):
    description = models.TextField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"Bills: {self.description} - {self.amount}"

# Other Expenses (if needed)
class OtherExpense(models.Model):
    description = models.TextField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"Other: {self.description} - {self.amount}"

# expenseapp/models.py
from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    monthly_budget = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.user.username}'s Profile"
