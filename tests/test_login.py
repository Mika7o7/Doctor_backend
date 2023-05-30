import json

import pytest
from django.test.client import Client

from api.models import Token, User

"Login test"


@pytest.mark.django_db
def test_login(client: Client) -> None:

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
    assert response.status_code == 202
    token = Token.objects.filter(user=user).first()
    assert content.get("token") == token.key  # type: ignore
    assert token.user.email_verified  # type: ignore
    assert not token.deleted  # type: ignore


@pytest.mark.django_db
def test_email_not_exitsts(client: Client) -> None:
    email = "test2@test.test"
    password = "123aaa123"
    mimetype = "application/json"
    headers = {"Content-Type": mimetype, "Accept": mimetype}
    data = {
        "email": email,
        "password": password,
    }
    response = client.post(
        "/auth/login/",
        data=data,
        headers=json.dumps(headers),
    )

    assert response.status_code == 400


@pytest.mark.django_db
def test_password_wrong(client: Client) -> None:
    email = "test2@test.test"
    password = "qwerty"
    User.objects.create(email=email, password="password")
    mimetype = "application/json"
    headers = {"Content-Type": mimetype, "Accept": mimetype}
    data = {
        "email": email,
        "password": password,
    }
    response = client.post(
        "/auth/login/",
        data=data,
        headers=json.dumps(headers),
    )
    content = json.loads(response.content)
    assert content == {
        "non_field_errors": ["Access denied: wrong username or password."]
    }
    assert response.status_code == 400
