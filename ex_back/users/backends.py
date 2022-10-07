from django.db.models import Q
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend


User = get_user_model()


class EmailOrUsernameBackend(BaseBackend):
    """Custom login backend that allows to auth via email or username."""

    def authenticate(self, request, username, password):
        try:
            user = User.objects.get(Q(username=username) | Q(email=username))
        except User.DoesNotExist:
            return None

        return user if user.check_password(password) else None  # type: ignore
