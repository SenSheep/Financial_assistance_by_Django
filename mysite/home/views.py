from django.shortcuts import render

def home(request):
    return render(request, 'home/home.html')

from django.shortcuts import render, redirect
from .forms import RegistrationForm

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Перенаправляем пользователя на страницу входа
    else:
        form = RegistrationForm()
    return render(request, 'home/register.html', {'form': form})

from django.contrib.auth import logout
def logout_view(request):
    logout(request)
    return redirect('home')

from .forms import TransactionForm
from django.contrib.auth.decorators import login_required

@login_required
def add_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            # Сохраняем транзакцию с привязкой к текущему пользователю
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            return redirect('profile')  # Перенаправление на страницу с транзакциями
    else:
        form = TransactionForm()

    return render(request, 'profile.html', {'form': form})

from django.shortcuts import render
from .models import Transaction
import matplotlib.pyplot as plt
import io
import base64
from django.contrib.auth.decorators import login_required
from django.db.models import Sum

@login_required
def profile(request):
    user = request.user
    user_id = user.id + 100 
    # Получаем транзакции текущего пользователя
    transactions = Transaction.objects.filter(user=user).order_by('-date')
    
    # Разделяем транзакции на прибыль и затраты
    income = transactions.filter(amount__gt=0)
    expenses = transactions.filter(amount__lt=0)

    # Суммируем по категориям для прибыли и затрат
    income_data = income.values('category').annotate(total_amount=Sum('amount'))
    expense_data = expenses.values('category').annotate(total_amount=Sum('amount'))

    # Генерация диаграммы для прибыли
    income_categories = [entry['category'] for entry in income_data]
    income_values = [entry['total_amount'] for entry in income_data]
    plt.figure(figsize=(6, 4))
    plt.bar(income_categories, income_values, color='green')
    plt.title("Profit by Category")
    plt.xlabel("Category")
    plt.ylabel("Amount")
    plt.tight_layout()

    # Сохранение диаграммы в base64
    income_img = io.BytesIO()
    plt.savefig(income_img, format='png')
    income_img.seek(0)
    income_chart = base64.b64encode(income_img.getvalue()).decode()

    # Генерация диаграммы для затрат
    expense_categories = [entry['category'] for entry in expense_data]
    expense_values = [entry['total_amount'] for entry in expense_data]
    plt.figure(figsize=(6, 4))
    plt.bar(expense_categories, expense_values, color='red')
    plt.title("Expenses by Category")
    plt.xlabel("Category")
    plt.ylabel("Amount")
    plt.tight_layout()

    # Сохранение диаграммы в base64
    expense_img = io.BytesIO()
    plt.savefig(expense_img, format='png')
    expense_img.seek(0)
    expense_chart = base64.b64encode(expense_img.getvalue()).decode()

    # Передаем данные в шаблон
    return render(request, 'home/profile.html', {
        'transactions': transactions,
        'income_chart': income_chart,
        'expense_chart': expense_chart,
        'user_id': user_id
    })