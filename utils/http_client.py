
from typing import Any

import requests


def login(username: str, password: str) -> dict[str, Any]:
    payload = {
        "login": username,
        "password": password,
    }
    timeout = 10
    base_url = "https://dev.api.oy-gul.uz/api/auth/login"

    response = requests.post(base_url, json=payload, timeout=timeout)
    response.raise_for_status()
    response_body = {
        "user_id": response.json()["data"]["userId"],
        "bearer_token": response.json()["data"]["token"],
        "refresh_token": response.cookies.get("refreshToken"),
    }
    user_info = get_user(response_body["user_id"], response_body["bearer_token"])
    response_body["merchant_id"] = user_info["merchantId"]
    response_body["branch_id"] = user_info["branchId"] or get_branch_id_by_merchant_id(response_body["merchant_id"], response_body["bearer_token"])
    return response_body


def get_user(user_id: str, token: str) -> dict[str, Any]:
    base_url = "https://dev.api.oy-gul.uz/api/auth/users/" + user_id
    headers = {"Authorization": f"Bearer {token}"}
    timeout = 10
    response = requests.get(base_url, headers=headers, timeout=timeout)
    response.raise_for_status()
    return response.json()


def get_branch_id_by_merchant_id(merchant_id: str, token: str) -> str:
    base_url = "https://dev.api.oy-gul.uz/api/auth/branch/getAll?merchantId=" + merchant_id
    headers = {"Authorization": f"Bearer {token}"}
    timeout = 10
    response = requests.get(base_url, headers=headers, timeout=timeout)
    response.raise_for_status()
    return response.json()["data"][0]["id"]

