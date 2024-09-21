from django.shortcuts import render, redirect
from .forms import ExpenseForm

def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('expense_list')  # Redirect to a list of expenses after saving
    else:
        form = ExpenseForm()
    return render(request, 'add_expense.html', {'form': form})

from .models import Expense


import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from io import BytesIO
import base64
from django.shortcuts import render
from .models import Expense

def expense_list(request):
    # Fetch all expenses
    expenses = Expense.objects.all()

    # Calculate the total expense
    total_expense = sum(expense.amount for expense in expenses)

    # Prepare data for the pie chart (Group expenses by category)
    categories = ['Food', 'Grocery/Stationary', 'Bills', 'Other']
    expense_data = {category: 0 for category in categories}
    
    for expense in expenses:
        expense_data[expense.get_category_display()] += expense.amount

    # Generate a 2D pie chart
    fig, ax = plt.subplots(figsize=(6, 6), facecolor='none')  # Set figure background to transparent
    wedges, texts, autotexts = ax.pie(
        expense_data.values(), 
        labels=expense_data.keys(), 
        autopct='%1.1f%%', 
        startangle=90, 
        explode=[0.05]*len(categories),
        shadow=True
    )

    # Set the text properties
    for text in texts:
        text.set_color('white')  # Color for the category labels
    for autotext in autotexts:
        autotext.set_color('black')  # Color for the percentage text
        autotext.set_size(12)

    # Animation function
    def animate(i):
        for wedge in wedges:
            wedge.set_alpha(0.7 + 0.3 * (i % 10 < 5))  # Pulse effect
        return wedges

    # Create the animation
    ani = FuncAnimation(fig, animate, frames=10, interval=200, blit=False)

    # Save the pie chart to a BytesIO buffer with a transparent background
    buffer = BytesIO()
    plt.savefig(buffer, format='png', transparent=True)
    buffer.seek(0)

    # Encode the chart to base64 to embed in the template
    chart_data = base64.b64encode(buffer.getvalue()).decode('utf-8')
    plt.close(fig)

    # Pass the expenses, total expense, and the chart to the template
    context = {
        'expenses': expenses,
        'total_expense': total_expense,
        'chart_data': chart_data,
    }

    return render(request, 'expense_list.html', context)

# expenseapp/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages

# Sign Up View
def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()  # Save the user
            messages.success(request, 'Your account has been created! You can now log in.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

# Login View

# Logout View
def logout_view(request):
    logout(request)
    return redirect('login')

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import ExpenseForm

# View for Home Page (Dashboard)
  # Ensure only logged-in users can access the home page
def home(request):
    return render(request, 'home.html')

# View for Login
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to the home page after successful login
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'login.html')
from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    return redirect('home')  # Redirect to login page after logout
