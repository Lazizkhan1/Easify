from google.adk.tools import ToolContext
import requests


def refresh_token(token: str, tool_context: ToolContext) -> dict[str, str] | None:
    """
    Refreshes the JWT token using the refreshToken.

    This tool should be used when other tools fail with a 401 Unauthorized error
    or an error message containing the word "token", indicating that the
    bearer token has expired. It will update the bearer_token and
    token in the tool_context state.
    """
    base_url = "https://dev.api.oy-gul.uz/api/auth/refresh"
    timeout = 10
    cookie = {"refreshToken": token}
    try:
        response = requests.post(url=base_url, cookies=cookie, timeout=timeout)
        response.raise_for_status()

        tool_context.state.update(
            {
                "refresh_token": response.cookies.get("refreshToken"),
                "bearer_token": response.json()["data"]["token"],
            }
        )
    except Exception as e:
        return {
            "status": "error",
            "message": f"error while refreshing the token {str(e)}"
        }
