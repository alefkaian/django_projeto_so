from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse

class RedirectAuthenticatedUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.path == reverse('login') and request.user.is_authenticated:
            if request.user.is_superuser:
                return redirect('admin:index')
            elif request.user.groups.filter(name='Gerenciamento').exists():
                return redirect('dashboard')
        return response
