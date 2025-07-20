from typing import Any, Dict
from google.adk.tools.tool_context import ToolContext
import requests
from datetime import datetime, timezone


def create_supply(
    tool_context: ToolContext,
    quantity: int,
    unit_cost: int,
    product_type: str,
    product_id: str,
) -> Dict[str, Any]:
    """
    Create a new supply record in the OyGul content service.

    Args:
        quantity (int): Quantity supplied.
        unit_cost (int): Cost per unit (in Uzbek so'ms, UZS).
        product_type (str): Type of product ('FLOWER', 'CONSUMABLE', 'SWEET').
        product_id (str): UUID of the product being supplied.

    Returns:
        dict: The parsed JSON response from the API, including the created supply's details.
    """
    try:
        branch_id = tool_context.state["branch_id"]
        token = tool_context.state.get("bearer_token")
        base_url = "https://dev.api.oy-gul.uz/api/content/supplies/"
        timeout = 10
        payload = {
            "branchId": branch_id,
            "supplyDate": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S"),
            "quantity": quantity,
            "unitCost": unit_cost,
            "productType": product_type,
            "productId": product_id,
        }
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.post(base_url, json=payload, headers=headers, timeout=timeout)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Failed to create supply: {str(e)}",
        }
