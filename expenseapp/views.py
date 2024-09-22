from django.shortcuts import render, redirect
from .forms import ExpenseForm
from .models import Expense
from django.db.models import Sum
import json
from django.contrib.auth.decorators import login_required


# expenseapp/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Sign Up View
def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been created! You can now log in.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

# Login View
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')  # Redirect to the dashboard after login
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

# Logout View
def logout_view(request):
    logout(request)
    return redirect('login')

# Dashboard View


from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Expense, MonthlyBudget
from django.db.models import Sum

@login_required
def dashboard_view(request):
    user = request.user
    total_expenses = Expense.objects.filter(user=user).aggregate(Sum('amount'))['amount__sum'] or 0
    monthly_budget = MonthlyBudget.objects.filter(user=user).first()
    
    budget_amount = monthly_budget.budget_amount if monthly_budget else 0
    remaining_budget = budget_amount - total_expenses

    # Ensure remaining budget is non-negative
    if remaining_budget < 0:
        remaining_budget = 0
    
    # Check if expenses exceed the budget
    budget_exceeded = total_expenses > budget_amount

    context = {
        'total_expenses': total_expenses,
        'monthly_budget': monthly_budget,
        'remaining_budget': remaining_budget,
        'budget_exceeded': budget_exceeded
    }
    
    return render(request, 'dashboard.html', context)



    


from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import ExpenseForm

@login_required
def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user  # Associate the expense with the logged-in user
            expense.save()
            return redirect('expense_list')
    else:
        form = ExpenseForm()
    return render(request, 'add_expense.html', {'form': form})


from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import MonthlyBudget, Expense
from .forms import MonthlyBudgetForm
from django.db.models import Sum

@login_required
def set_monthly_budget(request):
    current_month = timezone.now().date().replace(day=1)

    # Check if the budget is already set for this month
    try:
        budget = MonthlyBudget.objects.get(user=request.user, month=current_month)
        return redirect('dashboard')
    except MonthlyBudget.DoesNotExist:
        budget = None

    if request.method == 'POST':
        form = MonthlyBudgetForm(request.POST)
        if form.is_valid():
            budget_instance = form.save(commit=False)
            budget_instance.user = request.user
            budget_instance.month = current_month
            budget_instance.save()
            return redirect('dashboard')
    else:
        form = MonthlyBudgetForm()

    return render(request, 'set_monthly_budget.html', {'form': form})




from django.shortcuts import render
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import Expense, MonthlyBudget
from django.db.models import Sum

@login_required
def expense_list(request):
    current_month = timezone.now().date().replace(day=1)

    # Get all expenses for the current user in the current month
    expenses = Expense.objects.filter(user=request.user, date__month=current_month.month, date__year=current_month.year)

    # Calculate total expenses for the current month
    total_expenses = expenses.aggregate(Sum('amount'))['amount__sum'] or 0

    # Get the monthly budget for the current user
    try:
        budget = MonthlyBudget.objects.get(user=request.user, month=current_month)
        monthly_budget = budget.budget_amount
    except MonthlyBudget.DoesNotExist:
        monthly_budget = None

    # Get the expense totals by category for the pie chart
    category_expenses = expenses.values('category').annotate(total=Sum('amount'))

    # Prepare data for the pie chart
    categories = [entry['category'] for entry in category_expenses]
    totals = [float(entry['total']) for entry in category_expenses]

    context = {
        'expenses': expenses,
        'total_expenses': total_expenses,
        'monthly_budget': monthly_budget,
        'categories': categories,
        'totals': totals,
        'current_month': current_month,
    }

    return render(request, 'expense_list.html', context)


def index(request):
    return render(request, 'index.html')