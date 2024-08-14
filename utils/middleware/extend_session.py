from datetime import timedelta


class ExtendSessionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.user.is_authenticated:
            request.session.set_expiry(timedelta(days=365 * 5))
        return response

