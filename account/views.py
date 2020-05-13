from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User, Permission
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseGone, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.core.mail import send_mail
from django.conf import settings
from django.views.generic import ListView

from rest_framework.decorators import api_view


class Login(LoginView):
    template_name = 'account/login.html'
    redirect_authenticated_user = True

    def post(self, request, *args, **kwargs):
        remember_me = request.POST.get('remember-me')
        if remember_me == 'on':
            pass
        else:
            request.session.set_expiry(30 * 60)
        return super().post(request, *args, **kwargs)


class Logout(LogoutView):
    pass


@login_required
@require_http_methods(['POST'])
def change_pwd(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    new_password = request.POST.get('new-pass')
    user = authenticate(request=request, username=username, password=password)
    if user is not None:
        user.set_password(new_password)
        user.save()
        request.session.clear()
        return redirect(to=reverse(viewname='account:login'))
    else:
        return redirect(to=reverse(viewname='blog:dashboard:list-article'))


class ListUserView(LoginRequiredMixin, ListView):
    model = User
    ordering = ['username', 'first_name', 'last_name']
    context_object_name = 'users'
    template_name = 'account/user_list.html'


def add_user(request):
    username = request.POST['username']
    password = request.POST['password']
    if User.objects.filter(username__exact=username).exists():
        messages.add_message(request, messages.ERROR, 'User %s này đã tồn tại!' %username, 'danger')
        return redirect(to='account:list-user')
    user = User.objects.create_user(username=username, password=password)
    # Set permissions for user who will be saved
    add_articles = Permission.objects.get(codename__exact='add_articles')
    change_articles = Permission.objects.get(codename__exact='change_articles')
    user.user_permissions.add(add_articles, change_articles)
    user.save()
    return redirect(to='account:list-user')


@api_view(['POST'])
def check_login(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(request, username=username, password=password)
    if user is not None and user.is_active:
        return JsonResponse(data={'success':True}, status=202)