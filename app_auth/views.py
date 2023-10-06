from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from .forms import RegistrationForm

def login_view(request):
    redirect_url = reverse("profile")
    # когда пользователь заходит на страницу логина есть 2 варианта - он уже залогинен или нет 
    if request.method == "GET": 
        # если залогинен, перенаправляем его на страницу профиля
        if request.user.is_authenticated:
            return redirect(redirect_url)
        # иначе отображаем страницу с формой
        else:
            return render(request, "app_auth/login.html")
    # если 2 return не выполнились - то дошло до этих строк, а значит запрос был не GET
    # значит запрос был POST - получаем из него информацию - логин и пароль
    username = request.POST["username"] # получаем словарь и ищем там значение по ключу username
    password = request.POST["password"]
    # получили информацию из формы, проверяем пользователя в базе данных и пробуем произвести вход
    user = authenticate(request, username=username, password=password)
    # если такой пользователь есть и его пароль совпадает, нам вернется instance пользователя
    # а если нет то None
    if user is not None:
        login(request, user)
        return redirect(redirect_url)
    # если все верхние return не выполнились
    return render(request, "app_auth/login.html", context={"error": "Пользователь не найден"})

@login_required(login_url=reverse_lazy("login")) # reverse lazy - чтобы дать время странице прогрузится
def profile_view(request):
    return render(request, "app_auth/profile.html")

def logout_view(request):
    logout(request)
    return redirect(reverse("login"))


def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(reverse("profile"))
    else:
        form = RegistrationForm()
    return render(request, "app_auth/register.html", {'form':form})