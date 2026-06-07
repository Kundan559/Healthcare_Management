import threading

_local = threading.local()


class CurrentUserMiddleware:
    """Middleware that stores the current request user in a thread-local.

    This is a lightweight helper so signal handlers can record which user
    performed a change. Add `records.middleware.CurrentUserMiddleware` to
    `MIDDLEWARE` (after AuthenticationMiddleware).
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        _local.user = getattr(request, "user", None)
        try:
            return self.get_response(request)
        finally:
            if hasattr(_local, "user"):
                del _local.user


def get_current_user():
    return getattr(_local, "user", None)
