from django.contrib import auth
from django.shortcuts import render
from authapp.forms import ShopUserLoginForm, ShopUserRegisterForm, ShopUserUpdateForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings
from authapp.models import ShopUser


def login(request):
    next = request.GET.get('next', '')
    if request.method == 'POST':
        form = ShopUserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user and user.is_active:
                auth.login(request, user)
                if 'next' in request.POST.keys():
                    return HttpResponseRedirect(request.POST['next'])
                else:
                    return HttpResponseRedirect(reverse('main:index'))
    else:
        form = ShopUserLoginForm()
    context = {
        'title': 'вход в систему',
        'form': form,
        'next': next,
    }
    return render(request, 'authapp/login.html', context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('main:index'))


def register(request):
    if request.method == 'POST':
        form = ShopUserRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('main:index'))

    else:
        form = ShopUserRegisterForm()
    context = {
        'title': 'регистрация пользователя',
        'form': form,
    }
    return render(request, 'authapp/register.html', context)


def update(request):
    if request.method == 'POST':
        form = ShopUserUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('auth:update'))

    else:
        form = ShopUserUpdateForm(instance=request.user)
    context = {
        'title': 'Данные пользователя',
        'form': form,
    }
    return render(request, 'authapp/update.html', context)


def verify(request, email, key):
    pass


def send_verify_mail(user):
    verify_link = reverse('authapp:verify', args=[user.email, user.activate_key])
    full_link = f'{settings.BASE_URL}{verify_link}'

    message = f' Your activation url: \n{full_link}'

    send_mail(
        'Account activation',
        message,
        settings.EMAIL_HOST_USER,
        [user.email],
        fail_silently=False
    )
