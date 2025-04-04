from django.shortcuts import redirect
# from django_redis import get_redis_connection

def login_required_custom(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper
