from django import forms
from .models import Expense

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['category', 'description', 'amount', 'date']

from django import forms
from .models import MonthlyBudget

class MonthlyBudgetForm(forms.ModelForm):
    class Meta:
        model = MonthlyBudget
        fields = ['budget_amount']