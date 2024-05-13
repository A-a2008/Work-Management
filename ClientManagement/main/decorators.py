from django.shortcuts import redirect
from django.contrib.auth.models import Group
from functools import wraps

def login_required(redirect_to):
    def decorator(view_func):
        @wraps(view_func)
        def wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect(redirect_to)

            return view_func(request, *args, **kwargs)

        return wrapped_view
    return decorator


def group_required(group_name):
    def decorator(view_func):
        @wraps(view_func)
        def wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')
            
            if request.user.is_staff or request.user.is_superuser:
                return view_func(request, *args, **kwargs)

            group = Group.objects.get(name=group_name)
            if not group in request.user.groups.all():
                return redirect('no_access')  
            
            return view_func(request, *args, **kwargs)

        return wrapped_view
    return decorator
