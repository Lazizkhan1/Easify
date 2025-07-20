from typing import Any, Dict

import requests
from google.adk.tools.tool_context import ToolContext


def get_all_measurement_types(
    tool_context: ToolContext,
) -> Dict[str, Any]:
    """
    Retrieve all existing measurement types from the OyGul content service.

    Returns:
        dict: The parsed JSON response from the API, including all measurement type details.
    """
    try:
        lang = tool_context.state.get("lang")
        token = tool_context.state.get("bearer_token")
        base_url = "https://dev.api.oy-gul.uz/api/content/measurement-types"
        timeout = 10
        params = {}
        if lang is not None:
            params["lang"] = lang

        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(
            base_url, params=params, headers=headers, timeout=timeout
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Failed to get measurement types: {str(e)}",
        }
