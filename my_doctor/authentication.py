from rest_framework import exceptions
from rest_framework.authentication import TokenAuthentication

from api.models import Token


class CustomTokenAuthentication(TokenAuthentication):
    model = Token

    def authenticate_credentials(self, key):
        model = self.get_model()
        try:
            token = model.objects.select_related("user").get(key=key)
            if token.deleted:
                raise model.DoesNotExist()
        except model.DoesNotExist:
            raise exceptions.AuthenticationFailed("Invalid token.")

        if not token.user.is_active:
            raise exceptions.AuthenticationFailed("User inactive or deleted.")

        return (token.user, token)
