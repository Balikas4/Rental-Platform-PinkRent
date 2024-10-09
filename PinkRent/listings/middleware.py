from django.conf import settings
from django.utils import translation
from django.utils.deprecation import MiddlewareMixin

class LanguageMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get the language from the URL parameters or a form submission
        new_language = request.POST.get('language')  # Change this if your language switcher uses a different key

        if new_language:
            # Activate the selected language and save it in the session
            translation.activate(new_language)
            request.LANGUAGE_CODE = new_language
            request.session[settings.LANGUAGE_SESSION_KEY] = new_language
        else:
            # Check for an existing language in the session
            language = request.session.get(settings.LANGUAGE_SESSION_KEY)

            if language:
                translation.activate(language)
                request.LANGUAGE_CODE = language
            else:
                # Default to Lithuanian for unauthenticated users
                if not request.user.is_authenticated:
                    language = 'lt'
                    translation.activate(language)
                    request.LANGUAGE_CODE = language
                    request.session[settings.LANGUAGE_SESSION_KEY] = language  # Save in the session

        # Call the next middleware or view
        response = self.get_response(request)

        return response
