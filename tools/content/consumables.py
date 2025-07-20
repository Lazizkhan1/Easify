from typing import Any, Dict, List, Optional

import requests
from google.adk.tools.tool_context import ToolContext


def create_consumable_master(
    tool_context: ToolContext,
    name: dict,
    measurement_type_id: str,
    quantity: float,
    unit_cost: float,
    photo_urls: List[str],
) -> dict:
    """
    Create a new consumable (master) in the OyGul content service.

    Args:
        name (dict):
            Name of the consumable in multiple languages. Example:
                {
                    "uz": "master iste'mol qilinadigan",
                    "ru": "мастер расходник",
                    "en": "master consumable"
                }
        measurement_type_id (str):
            UUID of the measurement type for this consumable.
        quantity (float):
            Initial stock quantity for this consumable.
        unit_cost (float):
            Cost per unit (in Uzbek so'ms, UZS).
        photo_urls (list, optional):
            List of photo UUIDs for this consumable. Example:
                ["ac82585b-d15f-473b-a079-3264cb021dfb", ...]
            If not provided, no photos will be attached.

    Returns:
        dict: The parsed JSON response from the API, including the created consumable's details.

    Raises:
        requests.RequestException: If the HTTP request fails.
        ValueError: If the response cannot be parsed as JSON.
    """
    try:
        merchant_id = tool_context.state["merchant_id"]
        branch_id = tool_context.state["branch_id"]
        token = tool_context.state.get("bearer_token")
        base_url = "https://dev.api.oy-gul.uz/api/content/consumables/master/"
        timeout = 10
        payload = {
            "merchant_id": merchant_id,
            "branch_id": branch_id,
            "name": name,
            "measurement_type_id": measurement_type_id,
            "quantity": quantity,
            "unit_cost": unit_cost,
        }
        if photo_urls is not None:
            payload["photo_urls"] = photo_urls
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.post(
            base_url, json=payload, headers=headers, timeout=timeout
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Failed to create consumable (master): {str(e)}",
        }


def get_consumables(
    tool_context: ToolContext,
    search: Optional[str] = None,
    consumable_type_ids: Optional[List[str]] = None,
    consumable_ids: Optional[List[str]] = None,
    page: Optional[int] = None,
    limit: Optional[int] = None,
    sort: str = "updatedAt-desc",
) -> Dict[str, Any]:
    """
    Retrieve a paginated list of consumables from the OyGul content service.

    Args:
        search (str, optional):
            Search query for consumable names. Example: "tape"
        consumable_type_ids (List[str], optional):
            List of consumable_type_id to filter by.
        consumable_ids (List[str], optional):
            List of consumable_id to filter by.
        page (int, optional):
            Page number for pagination. Example: 1
        limit (int, optional):
            Number of items per page. Example: 20
        sort (str, optional):
            Sorting order. Format: '<field>-<direction>'. Default is 'updatedAt-desc'.
            Supported fields: 'createdAt', 'updatedAt', 'quantity', 'state', 'deletedAt'.
            Example values: 'updatedAt-desc', 'quantity-desc'.

    Returns:
        dict: The parsed JSON response from the API, including pagination and consumable details.

    Raises:
        requests.RequestException: If the HTTP request fails.
        ValueError: If the response cannot be parsed as JSON.
    """
    try:
        merchant_id = tool_context.state["merchant_id"]
        branch_id = tool_context.state["branch_id"]
        lang = tool_context.state.get("lang")
        token = tool_context.state.get("bearer_token")
        base_url = "https://dev.api.oy-gul.uz/api/content/consumables"
        timeout = 10
        params = {
            "merchant_id": merchant_id,
            "branch_id": branch_id,
        }
        if search is not None:
            params["search"] = search
        if consumable_type_ids is not None:
            params["type_id"] = consumable_type_ids
        if consumable_ids is not None:
            params["id"] = consumable_ids
        if lang is not None:
            params["lang"] = lang
        if page is not None:
            params["page"] = page
        if limit is not None:
            params["limit"] = limit
        if sort is not None:
            params["sort"] = sort

        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(
            base_url, params=params, headers=headers, timeout=timeout
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Failed to get consumables: {str(e)}",
        }


def update_consumable(
    tool_context: ToolContext,
    consumable_id: str,
    quantity: float,
) -> Dict[str, Any]:
    """
    Update consumable quantity.

    Args:
        consumable_id (str): The UUID of the consumable to update.
        quantity (float): New quantity value.

    Returns:
        dict: JSON response from API or error dictionary.
    """
    try:
        token = tool_context.state.get("bearer_token")
        base_url = f"https://dev.api.oy-gul.uz/api/content/consumables/{consumable_id}/"
        timeout = 10

        payload = {"quantity": quantity}

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        response = requests.put(base_url, headers=headers, json=payload, timeout=timeout)
        response.raise_for_status()
        return response.json()

    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Failed to update consumable: {str(e)}"
        }


def update_consumable_type(
    tool_context: ToolContext,
    consumable_type_id: str,
    name: Optional[dict] = None,
    measurement_type_id: Optional[str] = None,
    photo_urls: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """
    Update a consumable type in the OyGul content service.

    Args:
        consumable_type_id (str): The unique identifier of the consumable type to update.
        name (dict, optional): Name of the consumable type in multiple languages. Example:
            {
                "uz": "Yelim lenta",
                "ru": "Клейкая лента",
                "en": "Adhesive tape"
            }
        measurement_type_id (str, optional): UUID of the measurement type for this consumable type.
        photo_urls (list, optional): List of image UUIDs for the consumable type.

    Returns:
        dict: Parsed JSON response or error.
    """
    try:
        token = tool_context.state.get("bearer_token")
        base_url = f"https://dev.api.oy-gul.uz/api/content/consumable-types/{consumable_type_id}/"
        timeout = 10

        payload = {}
        if name is not None:
            payload["name"] = name
        if measurement_type_id is not None:
            payload["measurement_type_id"] = measurement_type_id
        if photo_urls is not None:
            payload["photo_urls"] = photo_urls

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        response = requests.put(base_url, json=payload, headers=headers, timeout=timeout)
        response.raise_for_status()
        return response.json()

    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Failed to update consumable type: {str(e)}",
        }


def delete_consumable_type(
    consumable_type_id: str,
    tool_context: ToolContext,
) -> Dict[str, Any]:
    """
    Deletes an existing consumable type by its ID (performs a soft delete).

    Args:
        consumable_type_id (str):
            The unique identifier (consumable_type_id) of the consumable type to be deleted.

    Returns:
        dict: A dictionary indicating the status of the deletion, typically containing
              a success message or an error.
    """
    try:
        token = tool_context.state.get("bearer_token")
        base_url = (
            f"https://dev.api.oy-gul.uz/api/content/consumable-types/{consumable_type_id}"
        )
        timeout = 10

        headers = {"Authorization": f"Bearer {token}"}
        response = requests.delete(base_url, headers=headers, timeout=timeout)
        response.raise_for_status()
        return {
            "status": "success",
            "message": f"consumable_type {consumable_type_id} deleted successfully.",
        }
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Failed to delete consumable_type: {str(e)}",
        }
