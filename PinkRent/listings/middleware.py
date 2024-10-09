# listings/middleware.py

from django.conf import settings
from django.utils import translation

class LanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Activate the default language for new users/sessions
        if not hasattr(request, 'user'):
            # Make sure the request has the user attribute
            request.user = None  # This is just a placeholder; it will be set by the AuthenticationMiddleware
        
        # Check if the user is not authenticated and language is not set
        if not request.user.is_authenticated and request.session.get(settings.LANGUAGE_SESSION_KEY) is None:
            translation.activate('lt')  # Default to Lithuanian
            request.LANGUAGE_CODE = 'lt'
            request.session[settings.LANGUAGE_SESSION_KEY] = 'lt'  # Save in the session
        
        # Call the next middleware or view
        response = self.get_response(request)
        
        return response
