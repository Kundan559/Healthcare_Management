from functools import wraps
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .utils import get_user_role


def allowed_users(allowed_roles=()):

    def decorator(view_func):

        @wraps(view_func)
        @login_required(login_url='login')
        def wrapper_func(request, *args, **kwargs):
            role = get_user_role(request.user)
            if request.user.is_superuser or role in allowed_roles:
                return view_func(request, *args, **kwargs)
            return redirect('dashboard')

        return wrapper_func

    return decorator