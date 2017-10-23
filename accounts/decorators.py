# -*- coding: utf-8 -*-
from django.contrib.auth.views import redirect_to_login
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator


def class_view_decorator(function_decorator):
    def simple_decorator(View):
        View.dispatch = method_decorator(function_decorator)(View.dispatch)
        return View

    return simple_decorator


def require_user(view_func):
    def wrapped(request, *args, **kwargs):
        if request.user.is_anonymous():
            path = request.build_absolute_uri()
            return redirect_to_login(path, reverse_lazy('login'))
        else:
            return view_func(request, *args, **kwargs)
    return wrapped


user_login_required = class_view_decorator(require_user)
