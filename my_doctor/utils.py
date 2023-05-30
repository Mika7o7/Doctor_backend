import base64
import hashlib
from typing import Optional

import requests

from .user_agent_parser.UserAgent import UserAgent


def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    # print(ip)
    # print("aaa")
    url = f"https://ipinfo.io/{ip}/json"
    # url = "https://ipinfo.io/46.70.174.152/json"

    data = requests.get(url).json()

    return data


def get_user_agent(request) -> Optional[UserAgent]:
    # Tries to get UserAgent objects from cache before constructing a UserAgent
    # from scratch because parsing regexes.yaml/json (ua-parser) is slow
    if not hasattr(request, "META"):
        return None

    ua_string = request.META.get("HTTP_USER_AGENT", "")

    if not isinstance(ua_string, str):
        ua_string = ua_string.decode("utf-8", "ignore")

    user_agent = UserAgent(ua_string)
    return user_agent


def encode_to_md5(user_email: str, user_date_joined: str):
    md5_data = hashlib.md5(
        user_email.encode() + user_date_joined.encode()
    )  # nosec
    return md5_data.hexdigest()


def encode_to_base64(user_id: int, md5_data: str) -> str:
    custom_token_for_email = base64.b64encode(
        f"{user_id};;{md5_data}".encode("utf-8")
    )
    return custom_token_for_email.decode("utf-8")


def decode_from_base64(data: str):
    user_id, _md5_data = (base64.b64decode(data).decode("utf-8")).split(";;")

    print(user_id, _md5_data)
    # id = id_and_md5_data[0]
    # md5_data = id_and_md5_data[1]
    return user_id, _md5_data
