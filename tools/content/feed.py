from typing import Any, Dict, List, Optional

import requests
from google.adk.tools.tool_context import ToolContext


def search_feed(
    tool_context: ToolContext,
    page: Optional[int] = None,
    limit: Optional[int] = None,
    product_type: Optional[str] = None,
    search: Optional[str] = None,
    min_price: Optional[int] = None,
    max_price: Optional[int] = None,
    sort: Optional[str] = None,
    has_discount: Optional[bool] = None,
    tags: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """
    Search the OyGul feed for products (bouquets, flowers, etc).

    Args:
        page (int):
            The page number to fetch (pagination). Starts from 1. Default is 1.
        limit (int):
            Number of items per page. Default is 20. Maximum is typically 100.
        product_type (str, optional):
            Filter by product type. Known possible values are:
                - 'BOUQUET': Bouquets
                - 'FLOWER': Individual flowers
                - 'SWEET': Sweets
                - 'SWEET_BOX': Sweet boxes
                - 'CONSUMABLE': Consumables
                - 'BOUQUET_TYPE': Bouquet types
                - 'FLOWER_TYPE': Flower types
                - 'SWEET_TYPE': Sweet types
                - 'SWEET_BOX_TYPE': Sweet box types
                - 'CONSUMABLE_TYPE': Consumable types
            If not provided, all product types are included.
        search (str, optional):
            Search query for product name or description. Performs a case-insensitive text search across available products.
        min_price (int, optional):
            Minimum price (inclusive) to filter products by price, in the smallest currency unit (unit is uzbek so'ms (UZS)).
        max_price (int, optional):
            Maximum price (inclusive) to filter products by price, in the smallest currency unit (unit is uzbek so'ms (UZS)).
        sort (str, optional):
            Sort order for results. Known possible values are:
                - 'price-ascending': Sort by price, ascending
                - 'price-descending': Sort by price, descending
                - 'createdAt-ascending': Sort by creation date, ascending
                - 'createdAt-descending': Sort by creation date, descending
                - 'updatedAt-ascending': Sort by update date, ascending
                - 'updatedAt-descending': Sort by update date, descending
                - 'rating-ascending': Sort by rating, ascending
                - 'rating-descending': Sort by rating, descending
            If not provided, the default is 'updatedAt-descending'.
        has_discount (bool, optional):
            If True, only products with a discount will be returned. If False, only products without a discount will be returned. If not provided, both discounted and non-discounted products are included.
        tags (List[str], optional):
            List of tags to filter products. Each tag should be a string. If provided, only products containing all specified tags will be returned. Tags are matched exactly. Example: ['Mono', 'Red']

    Returns:
        dict: The parsed JSON response from the API, including:
            - data: List of product dicts
            - total: Total number of products
            - limit: Items per page
            - page: Current page
            - pages: Total pages

    Raises:
        requests.RequestException: If the HTTP request fails.
        ValueError: If the response cannot be parsed as JSON.
    """
    try:
        # Set default values for page and limit if not provided
        if page is None:
            page = 1
        if limit is None:
            limit = 20

        merchant_id = tool_context.state.get("merchant_id")

        base_url = "https://dev.api.oy-gul.uz/api/content/feed"
        timeout = 10
        params = {
            "page": page,
            "limit": limit,
            "lang": tool_context.state.get("user_language", "ru"),
        }
        if merchant_id:
            params["merchant_id"] = merchant_id
        if product_type:
            params["product_type"] = product_type
        if search:
            params["search"] = search
        if min_price is not None:
            params["min_price"] = min_price
        if max_price is not None:
            params["max_price"] = max_price
        if sort:
            params["sort"] = sort
        if has_discount is not None:
            params["has_discount"] = str(has_discount).lower()
        if tags:
            params["tags"] = ",".join(tags)
        response = requests.get(url=base_url, params=params, timeout=timeout)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Failed to search feed: {str(e)}",
        }
