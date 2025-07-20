from typing import Any, Dict, List, Optional

import requests
from google.adk.tools.tool_context import ToolContext


def create_flower_master(
    name: dict,
    description: dict,
    quantity: int,
    unit_cost: int,
    price: int,
    sold_separately: bool,
    sold_online: bool,
    photo_urls: List[str],
    tool_context: ToolContext,
) -> Dict[str, Any]:
    """
    Create a new flower (master) in the OyGul content service.

    Args:
        name (dict):
            Name of the flower in multiple languages. Example:
                {
                    "uz": "master gul",
                    "ru": "мастер цветок",
                    "en": "master flower"
                }
        description (dict):
            Description of the flower in multiple languages. Example:
                {
                    "uz": "type bilan produkt",
                    "ru": "type с продуктом",
                    "en": "type with product"
                }
        quantity (int):
            Initial stock quantity for this flower.
        unit_cost (int):
            Cost per unit (in Uzbek so'ms, UZS).
        price (int):
            Selling price per unit (in Uzbek so'ms, UZS).
        sold_separately (bool, optional):
            Whether this flower can be sold separately. Default is False.
        sold_online (bool, optional):
            Whether this flower is available for online sale. Default is True.
        photo_urls (List[str], optional):
            List of photo UUIDs for this flower. Example:
                ["ac82585b-d15f-473b-a079-3264cb021dfb", ...]
            If not provided, no photos will be attached.

    Returns:
        dict: The parsed JSON response from the API, including the created flower's details.

    Raises:
        requests.RequestException: If the HTTP request fails.
        ValueError: If the response cannot be parsed as JSON.
    """
    try:
        merchant_id = tool_context.state["merchant_id"]
        branch_id = tool_context.state["branch_id"]
        token = tool_context.state.get("bearer_token")
        base_url = "https://dev.api.oy-gul.uz/api/content/flowers/master/"
        timeout = 10
        payload = {
            "merchant_id": merchant_id,
            "branch_id": branch_id,
            "name": name,
            "description": description,
            "quantity": quantity,
            "unit_cost": unit_cost,
            "price": price,
            "sold_separately": sold_separately,
            "sold_online": sold_online,
            "photo_urls": photo_urls,
            "tags": [],
            "consumables": [],
        }
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.post(
            base_url, json=payload, headers=headers, timeout=timeout
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Failed to create flower (master): {str(e)}",
        }


def get_flowers(
    tool_context: ToolContext,
    search: Optional[str] = None,
    flower_type_ids: Optional[List[str]] = None,
    flower_ids: Optional[List[str]] = None,
    page: Optional[int] = None,
    limit: Optional[int] = None,
    sort: str = "updatedAt-desc",
) -> Dict[str, Any]:
    """
    Retrieve a paginated list of flowers from the OyGul content service.

    Args:
        search (str, optional):
            Search query for flower names or descriptions. Example: "rose"
        flower_type_ids (List[str], optional):
            List of flower_type_id to filter by.
        flower_ids (List[str], optional):
            List of flower_id to filter by.
        page (int, optional):
            Page number for pagination. Example: 1
        limit (int, optional):
            Number of items per page. Example: 20
        sort (str, optional):
            Sorting order. Format: '<field>-<direction>'. Default is 'updatedAt-desc'.
            Supported fields: 'createdAt', 'updatedAt', 'price', 'quantity', 'state', 'deletedAt'.
            Example values: 'updatedAt-desc', 'price-asc', 'quantity-desc'.

    Returns:
        dict: The parsed JSON response from the API, including pagination and flower details.

    Raises:
        requests.RequestException: If the HTTP request fails.
        ValueError: If the response cannot be parsed as JSON.
    """
    try:
        merchant_id = tool_context.state["merchant_id"]
        branch_id = tool_context.state["branch_id"]
        lang = tool_context.state.get("lang")
        token = tool_context.state.get("bearer_token")
        base_url = "https://dev.api.oy-gul.uz/api/content/flowers"
        timeout = 10
        params = {
            "merchant_id": merchant_id,
            "branch_id": branch_id,
        }
        if search is not None:
            params["search"] = search
        if flower_type_ids is not None:
            params["type_id"] = flower_type_ids
        if flower_ids is not None:
            params["id"] = flower_ids
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
            "error_message": f"Failed to get flowers: {str(e)}",
        }


def update_flower(
    tool_context: ToolContext,
    flower_id: str,
    quantity: int,
    price: Optional[int] = None,
    sold_separately: Optional[bool] = None,
    sold_online: Optional[bool] = None,
) -> Dict[str, Any]:
    """
    Update flower master fields such as quantity, price, and availability.

    Args:
        flower_id (str): The UUID of the flower to update. It is not flower_type_id.
        quantity (int): Optional new quantity.
        price (int, optional): Optional new price.
        sold_separately (bool, optional): Optional flag for separate sale.
        sold_online (bool, optional): Optional flag for online sale.

    Returns:
        dict: JSON response from API or error dictionary.
    """
    try:
        token = tool_context.state.get("bearer_token")
        base_url = f"https://dev.api.oy-gul.uz/api/content/flowers/{flower_id}/"
        timeout = 10

        payload = {"quantity": quantity}

        if price is not None:
            payload["price"] = price
        if sold_separately is not None:
            payload["sold_separately"] = sold_separately
        if sold_online is not None:
            payload["sold_online"] = sold_online

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
            "error_message": f"Failed to update flower master: {str(e)}"
        }


def update_flower_type(
    tool_context: ToolContext,
    flower_type_id: str,
    name: Optional[dict] = None,
    description: Optional[dict] = None,
    photo_urls: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """
    Update a flower type in the OyGul content service. if cannot be updated with update_flower, use this.

    Args:
        flower_type_id (str):The unique identifier (flower_type_id) of the flower type to be deleted.
        name (dict): Name of the flower in multiple languages. Example:
                {
                    "uz": "Akmal",
                    "ru": "Акамаль",
                    "en": "Akmal"
                }.
        photo_urls (list): List of image UUIDs for the flower.
        description (dict):
            Description of the flower in multiple languages. Example:
                {
                    "uz": "type bilan produkt",
                    "ru": "type с продуктом",
                    "en": "type with product"
                }

    Returns:
        dict: Parsed JSON response or error.
    """
    try:
        token = tool_context.state.get("bearer_token")
        base_url = f"https://dev.api.oy-gul.uz/api/content/flower-types/{flower_type_id}/"
        timeout = 10

        payload = {
            "name": name,
            "photo_urls": photo_urls,
        }

        if description is not None:
            payload["description"] = description

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
            "error_message": f"Failed to update flower (master): {str(e)}",
        }


def delete_flower_type(
    flower_type_id: str,
    tool_context: ToolContext,
) -> Dict[str, Any]:
    """
    Deletes an existing flower_type (with its flower) by its ID (performs a soft delete).

    Args:
        flower_type_id (str):
            The unique identifier (flower_type_id) of the flower_type to be deleted.

    Returns:
        dict: A dictionary indicating the status of the deletion, typically containing
              a success message or an error.

    Raises:
        requests.RequestException: If the HTTP request fails.
        ValueError: If the response cannot be parsed as JSON.
    """
    try:
        token = tool_context.state.get("bearer_token")
        base_url = (
            f"https://dev.api.oy-gul.uz/api/content/flower-types/{flower_type_id}"
        )
        timeout = 10

        headers = {"Authorization": f"Bearer {token}"}
        response = requests.delete(base_url, headers=headers, timeout=timeout)
        response.raise_for_status()
        return {
            "status": "success",
            "message": f"flower_type {flower_type_id} deleted successfully.",
        }
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Failed to delete flower_type: {str(e)}",
        }
