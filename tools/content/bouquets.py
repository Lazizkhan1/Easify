from typing import Any, Dict, List, Optional

import requests
from google.adk.tools.tool_context import ToolContext


def create_bouquet_master(
    name: dict,
    description: dict,
    price: int,
    sold_online: bool,
    photo_urls: List[str],
    tags: List[dict],
    products_spent: List[dict],
    tool_context: ToolContext,
) -> dict:
    """
    Create a new bouquet (master) in the OyGul content service.

    Args:
        name (dict):
            Name of the bouquet in multiple languages. Example:
                {
                    "uz": "master buket",
                    "ru": "мастер букет",
                    "en": "master bouquet"
                }
        description (dict):
            Description of the bouquet in multiple languages. Example:
                {
                    "uz": "type bilan produkt",
                    "ru": "type с продуктом",
                    "en": "type with product"
                }
        price (int):
            Selling price per unit (in Uzbek so'ms, UZS).
        sold_online (bool):
            Whether this bouquet is available for online sale.
        photo_urls (List[str]):
            List of photo UUIDs for this bouquet. Example:
                ["ac82585b-d15f-473b-a079-3264cb021dfb", ...]
        tags (List[dict]):
            List of tags in multiple languages. Example:
                [{"uz": "yangi", "ru": "новый", "en": "new"}, ...]
        products_spent (List[dict]):
            List of products spent to create this bouquet. Each dict should have keys: type_id (UUID), quantity (float), type (str: "FLOWER", "SWEET", etc.)

    Returns:
        dict: The parsed JSON response from the API, including the created bouquet's details.

    Raises:
        requests.RequestException: If the HTTP request fails.
        ValueError: If the response cannot be parsed as JSON.
    """
    try:
        merchant_id = tool_context.state["merchant_id"]
        branch_id = tool_context.state["branch_id"]
        token = tool_context.state.get("bearer_token")
        base_url = "https://dev.api.oy-gul.uz/api/content/bouquets/master/"
        timeout = 10
        payload = {
            "merchant_id": merchant_id,
            "branch_id": branch_id,
            "name": name,
            "description": description,
            "price": price,
            "sold_online": sold_online,
            "photo_urls": photo_urls,
            "tags": tags,
            "products_spent": products_spent,
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
            "error_message": f"Failed to create bouquet (master): {str(e)}",
        }


def get_bouquets(
    tool_context: ToolContext,
    search: Optional[str] = None,
    bouquet_type_ids: Optional[List[str]] = None,
    bouquet_ids: Optional[List[str]] = None,
    lang: Optional[str] = None,
    page: Optional[int] = None,
    limit: Optional[int] = None,
    sort: str = "updatedAt-desc",
) -> dict:
    """
    Retrieve a paginated list of bouquets from the OyGul content service.

    Args:
        search (str, optional):
            Search query for bouquet names or descriptions. Example: "wedding"
        bouquet_type_ids (List[str], optional):
            List of bouquet type UUIDs to filter by.
        bouquet_ids (List[str], optional):
            List of bouquet UUIDs to filter by.
        lang (str, optional):
            Language code for translations (e.g., 'uz', 'ru', 'en').
        page (int, optional):
            Page number for pagination. Example: 1
        limit (int, optional):
            Number of items per page. Example: 20
        sort (str, optional):
            Sorting order. Format: '<field>-<direction>'. Default is 'updatedAt-desc'.
            Supported fields: 'createdAt', 'updatedAt', 'price', 'quantity', 'state', 'deletedAt'.
            Example values: 'updatedAt-desc', 'price-asc', 'quantity-desc'.

    Returns:
        dict: The parsed JSON response from the API, including pagination and bouquet details.

    Raises:
        requests.RequestException: If the HTTP request fails.
        ValueError: If the response cannot be parsed as JSON.
    """
    try:
        merchant_id = tool_context.state["merchant_id"]
        branch_id = tool_context.state["branch_id"]
        token = tool_context.state.get("bearer_token")
        base_url = "https://dev.api.oy-gul.uz/api/content/bouquets"
        timeout = 10
        params = {
            "merchant_id": merchant_id,
            "branch_id": branch_id,
        }
        if search is not None:
            params["search"] = search
        if bouquet_type_ids is not None:
            params["type_id"] = bouquet_type_ids
        if bouquet_ids is not None:
            params["id"] = bouquet_ids
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
            "error_message": f"Failed to get bouquets: {str(e)}",
        }


def update_bouquet(
    tool_context: ToolContext,
    bouquet_id: str,
    quantity: Optional[int] = None,
    price: Optional[int] = None,
    sold_online: Optional[bool] = None,
) -> Dict[str, Any]:
    """
    Update bouquet fields such as quantity, price, and sold_online.

    Args:
        bouquet_id (str): The UUID of the bouquet to update.
        quantity (int, optional): New quantity.
        price (int, optional): New price.
        sold_online (bool, optional): New online sale flag.

    Returns:
        dict: JSON response from API or error dictionary.
    """
    try:
        token = tool_context.state.get("bearer_token")
        base_url = f"https://dev.api.oy-gul.uz/api/content/bouquets/{bouquet_id}/"
        timeout = 10
        payload = {}
        if quantity is not None:
            payload["quantity"] = quantity
        if price is not None:
            payload["price"] = price
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
            "error_message": f"Failed to update bouquet: {str(e)}"
        }


def update_bouquet_type(
    tool_context: ToolContext,
    bouquet_type_id: str,
    name: Optional[dict] = None,
    description: Optional[dict] = None,
    tags: Optional[List[dict]] = None,
    photo_urls: Optional[List[str]] = None,
    products_spent: Optional[List[dict]] = None,
) -> Dict[str, Any]:
    """
    Update a bouquet type (master) in the OyGul content service.

    Args:
        bouquet_type_id (str): The UUID of the bouquet type to update.
        name (dict, optional): Name translations, e.g. {"uz": "Buket", "ru": "Букет", "en": "Bouquet"}.
        description (dict, optional): Description translations.
        tags (List[dict], optional): List of tag translations, e.g. [{"uz": "yangi", "ru": "новый", "en": "new"}].
        photo_urls (List[str], optional): List of photo UUIDs.
        products_spent (List[dict], optional): List of dicts, each with keys: type_id (UUID), quantity (float), type (str: "FLOWER", etc.)

    Returns:
        dict: JSON response from API or error dictionary.
    """
    try:
        token = tool_context.state.get("bearer_token")
        base_url = f"https://dev.api.oy-gul.uz/api/content/bouquet-types/{bouquet_type_id}/"
        timeout = 10
        payload = {}
        if name is not None:
            payload["name"] = name
        if description is not None:
            payload["description"] = description
        if tags is not None:
            payload["tags"] = tags
        if photo_urls is not None:
            payload["photo_urls"] = photo_urls
        if products_spent is not None:
            payload["products_spent"] = products_spent
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
            "error_message": f"Failed to update bouquet type: {str(e)}"
        }


def delete_bouquet_type(
    bouquet_type_id: str,
    tool_context: ToolContext,
) -> dict:
    """
    Deletes an existing bouquet_type (with its bouquet) by its ID (soft delete).

    Args:
        bouquet_type_id (str):
            The unique identifier of the bouquet_type to be deleted.

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
            f"https://dev.api.oy-gul.uz/api/content/bouquet-types/{bouquet_type_id}"
            )
        timeout = 10

        headers = {"Authorization": f"Bearer {token}"}
        response = requests.delete(base_url, headers=headers, timeout=timeout)
        response.raise_for_status()
        return {
            "status": "success",
            "message": f"bouquet_type {bouquet_type_id} deleted successfully.",
        }
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Failed to delete bouquet_type: {str(e)}",
        }
