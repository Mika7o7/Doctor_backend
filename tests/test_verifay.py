import json

import pytest
from django.test.client import Client

from api.models import User
from my_doctor.utils import encode_to_base64, encode_to_md5


@pytest.mark.django_db
def test_verification(client: Client):
    email = "test2@test.test"
    password = "123aaa123"
    mimetype = "application/json"
    headers = {"Content-Type": mimetype, "Accept": mimetype}
    user = User.objects.create_user(email=email, password=password)

    decode_md5_data = encode_to_md5(
        user_email=email,
        user_date_joined=str(user.date_joined),
    )
    hash_data = encode_to_base64(
        user_id=user.id,
        md5_data=decode_md5_data,
    )

    response = client.get(
        f"/activate/{hash_data}/",
        headers=json.dumps(headers),
    )
    print(response.__dict__)
    assert response.status_code == 302
    user = User.objects.get(id=user.id)
    assert user.email_verified
