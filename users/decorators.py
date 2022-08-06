from django.shortcuts import redirect
from django.core.handlers.wsgi import WSGIRequest


def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if type(request) == WSGIRequest:
            if request.user.is_authenticated:
                return redirect('place_list')
        elif type(args[0]) == WSGIRequest:
            if args[0].user.is_authenticated:
                return redirect('place_list')
        return view_func(request, *args, **kwargs)
    return wrapper_func
