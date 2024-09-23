from django.shortcuts import render, redirect
from .models import Budget, Expense, Savings, Wishlist, Reminder
from django.db.models import Sum
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
import base64
from io import BytesIO

def generate_expense_pie_chart(expenses):
    categories = expenses.values_list('category', flat=True).distinct()
    amounts = [expenses.filter(category=category).aggregate(Sum('amount'))['amount__sum'] for category in categories]
    
    fig, ax = plt.subplots()
    ax.pie(amounts, labels=categories, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    ax.set_title('Expenses by Category')

    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    image_base64 = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()

    plt.close(fig)
    return image_base64
import matplotlib.pyplot as plt
import pandas as pd
import base64
from io import BytesIO
from django.db.models import Sum
from .models import Expense
from django.db.models.functions import ExtractMonth, ExtractYear 

def generate_monthly_expense_bar_chart(expenses):
    try:
        # Query all expenses
        all_expenses = expenses.annotate(month=ExtractMonth('created_at'), year=ExtractYear('created_at'))
        monthly_expenses = all_expenses.values('year', 'month').annotate(total_amount=Sum('amount'))

        # Prepare data for plotting
        months = []
        amounts = []
        for expense in monthly_expenses:
            months.append(f"{expense['year']}-{expense['month']}")
            amounts.append(expense['total_amount'])

        # Create DataFrame
        df = pd.DataFrame({'Month': months, 'Total Amount': amounts})
        df['Month'] = pd.to_datetime(df['Month'], format='%Y-%m')
        df.sort_values('Month', inplace=True)

        # Plotting
        fig, ax = plt.subplots()
        ax.bar(df['Month'], df['Total Amount'], width=10, align='center')
        ax.set_title('Monthly Expenses')
        ax.set_xlabel('Month')
        ax.set_ylabel('Amount')

        # Convert plot to base64 to embed in HTML
        buf = BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        image_base64 = base64.b64encode(buf.read()).decode('utf-8')
        buf.close()

        plt.close(fig)
        return image_base64

    except Exception as e:
        print("Exception occurred:", str(e))
        return None



def home(request):
    if request.method == 'POST':
        if 'budget' in request.POST:
            amount = request.POST['budget']
            Budget.objects.update_or_create(id=1, defaults={'amount': amount})
        
        if 'expense_description' in request.POST:
            description = request.POST['expense_description']
            amount = request.POST['expense_amount']
            category = request.POST['expense_category']
            Expense.objects.create(description=description, amount=amount, category=category)
        
        if 'savings' in request.POST:
            amount = request.POST['savings']
            Savings.objects.update_or_create(id=1, defaults={'amount': amount})
        
        if 'wishlist_description' in request.POST:
            description = request.POST['wishlist_description']
            amount = request.POST['wishlist_amount']
            Wishlist.objects.create(description=description, amount=amount)
        
        if 'remainder_description' in request.POST:
            description = request.POST['remainder_description']
            due_date = request.POST['remainder_date']
            Reminder.objects.create(description=description, due_date=due_date)
        
        return redirect('home')
    
    budget = Budget.objects.first()
    expenses = Expense.objects.all()
    savings = Savings.objects.all()
    wishlists = Wishlist.objects.all()
    reminders = Reminder.objects.all()

    total_expenses = expenses.aggregate(Sum('amount'))['amount__sum'] or 0
    remaining_budget = budget.amount - total_expenses if budget else None

    unimportant_expenses_total = expenses.filter(category='unimportant').aggregate(Sum('amount'))['amount__sum'] or 0
    alert_message = None
    if unimportant_expenses_total >= total_expenses / 2:
        alert_message = "Be mindful about the money you're spending more on unimportant things than savings."

    # Generate the charts
    expense_pie_chart = generate_expense_pie_chart(expenses)
    expense_bar_graph = generate_monthly_expense_bar_chart(expenses)

    context = {
        'budget': budget,
        'remaining_budget': remaining_budget,
        'expenses': expenses,
        'savings': savings,
        'wishlists': wishlists,
        'reminders': reminders,
        'alert_message': alert_message,
        'expense_pie_chart': expense_pie_chart,
        'expense_bar_graph':expense_bar_graph,
    }

    return render(request, 'home.html', context)
