from django.middleware.csrf import CsrfViewMiddleware

class CsrfExemptSessionAuthentication:
    def enforce_csrf(self, request):
        return