from django.contrib import admin
from django.urls import path, include
#from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('expenses/', include('expenseapp.urls')),
    #path('expense_list/', views.expense_list, name='expense_list'),  # Link the app's URLs
]
