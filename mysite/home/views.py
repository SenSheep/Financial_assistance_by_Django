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

from django.contrib.auth.decorators import login_required
from .models import Transaction

@login_required
def profile(request):
    user = request.user  # Получаем текущего пользователя
    user_id = user.id + 100  # Получаем его уникальный ID
    transactions = Transaction.objects.filter(user=user).order_by('-date')  # Получаем транзакции текущего пользователя
    return render(request, 'home/profile.html', {'transactions': transactions, 'user_id': user_id})

from django.contrib.auth import logout
def logout_view(request):
    logout(request)
    return redirect('home')

from .forms import TransactionForm
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