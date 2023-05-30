import json
from typing import Optional

import pytest
from django.test.client import Client

from api.models import Token, User

from .mock.mock_user import create_user_data

"Test our registretion seqtion with /auth/register/"


@pytest.mark.django_db
def test_register(client: Client) -> None:
    mimetype = "application/json"
    headers = {"Content-Type": mimetype, "Accept": mimetype}
    data = create_user_data()
    response = client.post(
        "/auth/register/",
        data=data,
        headers=json.dumps(headers),
    )
    content = json.loads(response.content)
    assert content.get("email") == data["email"]
    token: Optional[Token] = Token.objects.filter(
        user__email=data["email"]
    ).first()
    assert content.get("token") == token.key  # type: ignore
    assert not token.deleted  # type: ignore
    assert not token.user.email_verified  # type: ignore
    assert response.status_code == 201


@pytest.mark.django_db
def test_email_exists(client: Client) -> None:
    mimetype = "application/json"
    headers = {"Content-Type": mimetype, "Accept": mimetype}
    data = create_user_data()
    User.objects.create(email=data["email"], password=data["password"])
    response = client.post(
        "/auth/register/",
        data=data,
        headers=json.dumps(headers),
    )
    content = json.loads(response.content)
    assert "email" in content
    assert len(content) == 1
    assert response.status_code == 400


@pytest.mark.django_db
def test_password_invalid(client: Client) -> None:
    mimetype = "application/json"
    headers = {"Content-Type": mimetype, "Accept": mimetype}
    data = create_user_data(password="qwerty")
    response = client.post(
        "/auth/register/",
        data=data,
        headers=json.dumps(headers),
    )
    content = json.loads(response.content)
    assert "password" in content
    assert len(content) == 1
    assert len(content["password"]) > 1
    assert response.status_code == 400
