import datetime
from django.conf import settings
from django.contrib import auth
from django.shortcuts import redirect
from django.contrib import messages

class SessionIdleTimeoutMiddleware:
    """
    Déconnecte l'utilisateur après X secondes d'inactivité.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            now = datetime.datetime.now()
            last_activity = request.session.get("last_activity")

            if last_activity:
                elapsed = (now - datetime.datetime.fromisoformat(last_activity)).seconds
                if elapsed > getattr(settings, "SESSION_IDLE_TIMEOUT", 120):  # défaut 2 min
                    auth.logout(request)
                    messages.error(request, "⏳ Votre session a expiré pour cause d'inactivité.")
                    return redirect("login")  # adapte avec le nom de ta vue login

            # mettre à jour l'activité
            request.session["last_activity"] = now.isoformat()

        return self.get_response(request)
