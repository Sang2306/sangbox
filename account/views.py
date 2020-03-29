from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseGone
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.core.mail import send_mail
from django.conf import settings


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


def reset_password(request):
    send_mail(
        subject="Testing thoi",
        message='hello ban sang',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=['sang.tanhle@gmail.com'],
    )
    return HttpResponseGone()
