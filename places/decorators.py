from django.shortcuts import redirect
from django.core.handlers.wsgi import WSGIRequest


def check_groups(user, allowed_roles):
    group = None
    if user.groups.exists():
        group = user.groups.all()[0].name

    if group in allowed_roles:
        return True
    return False


def allwed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            if type(request) == WSGIRequest:
                user = request.user
                if check_groups(user, allowed_roles):
                    return view_func(request, *args, kwargs)
                #
                #
                # if request.user.groups.exist():
                #     group = request.user.groups.all()[0].name
                #
                # if group in allowed_roles:
                #     view_func(request, *args, kwargs)
                return redirect('place_list')

            elif type(args[0]) == WSGIRequest:
                user = args[0].user
                if check_groups(user, allowed_roles):
                    return view_func(request, *args, kwargs)
                return redirect('place_list')

        return wrapper_func

    return decorator
