import json

import pytest
from django.test.client import Client

from api.models import Token, User


@pytest.mark.django_db
def test_logout(client: Client) -> None:
    email = "test2@test.test"
    password = "123aaa123"
    mimetype = "application/json"
    headers = {"Content-Type": mimetype, "Accept": mimetype}

    data = {
        "email": email,
        "password": password,
    }
    user = User.objects.create_user(email=email, password=password)
    user.email_verified = True
    user.save()
    response = client.post(
        "/auth/login/",
        data=data,
        headers=json.dumps(headers),
    )
    content = json.loads(response.content)

    token_key = content.get("token")

    assert user.token.filter(key=token_key).exists()

    headers = {"HTTP_AUTHORIZATION": f"Token {token_key}"}
    response = client.post(
        "/auth/logout/",
        content_type=mimetype,
        **headers,
    )
    assert response.status_code == 200
    token = Token.objects.get(key=token_key)
    assert token.deleted
