from typing import Optional, List, Dict, Any

from google.adk.tools import ToolContext
import requests


def create_order(
        products: List[dict],
        payment_type: str,
        gift_card_note: Optional[str],
        tool_context: ToolContext,
) -> Dict[str, Any]:
    """Creates a new order in the OyGul transaction service.

    Args:
        products (List[dict]):
            A list of product dictionaries to be included in the order.
            Example:
                [
                    {
                        "productId": "8f38db18-0930-4fa4-8e75-a5fe7a552475",
                        "typeId": "d97382a8-7f7e-46fa-a69d-bbb4cb63733d",
                        "quantity": 1.0,
                        "productType": "BOUQUET",
                        "price": 446000.00
                    }
                ]

        payment_type (str):
            The method of payment for the order.
            Example: "CLICK"

        gift_card_note (str, optional):
            A note to be included with the gift card, if any.
            Example: "Happy Birthday!"

    Returns:
        dict: The parsed JSON response from the API, including the created order's details.

    Raises:
        requests.RequestException: If the HTTP request fails.
        ValueError: If the response cannot be parsed as JSON.
    """
    try:
        user_id = tool_context.state["user_id"]
        merchant_id = tool_context.state['merchant_id']
        branch_id = tool_context.state['branch_id']

        base_url = "https://dev.api.oy-gul.uz/api/transaction/orders"
        timeout = 10
        headers = {"Authorization": f"Bearer {tool_context.state['bearer_token']}"}
        payload = {
            "userId": user_id,
            "merchantId": merchant_id,
            "branchId": branch_id,
            "paymentType": payment_type,
            "products": products,
            "giftCardNote": gift_card_note,
        }

        response = requests.post(url=base_url, json=payload, headers=headers, timeout=timeout)
        response.raise_for_status()
        return response.json()

    except Exception as e:
        print(str(e))
        return {
            "status": "error",
            "error_message": f"Failed to create order: {str(e)}",
        }


def get_payment_types(tool_context: ToolContext) -> list[dict[str, str]] | dict[str, Any] | None:
    """Retrieves a list of available payment types from the OyGul transaction service.

    Args:
        None

    Returns:
        list: A list of dictionaries, where each dictionary represents a payment type.
              Example:
                [
                    {"name": "CASH"},
                    {"name": "UZCARD"},
                    ...
                ]

    Raises:
        requests.RequestException: If the HTTP request fails.
        ValueError: If the response cannot be parsed as JSON.
    """
    base_url = "https://dev.api.oy-gul.uz/api/transaction/payment-types"
    headers = {"Authorization": f"Bearer {tool_context.state['bearer_token']}"}
    timeout = 10

    try:
        response = requests.get(base_url, headers=headers, timeout=timeout)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Failed to get payment types: {str(e)}",
        }


def get_orders_by_status(
        status: str,
        tool_context: ToolContext,
        page: Optional[int] = None,
        limit: Optional[int] = None
) -> list[dict[str, Any]] | dict[str, str] | None:
    """Retrieves a list of orders from the OyGul transaction service, filtered by status.

    Args:
        status (str):
            The status of the orders to retrieve.
            Valid values are "PENDING", "FAILED", "CANCELED", "REFUND", "SUCCESSFUL".

    Returns:
        list: A list of dictionaries, where each dictionary represents an order.
        dict: An error dictionary if the request fails.
    """
    status = status.upper()
    statuses = ["PENDING", "FAILED", "CANCELED", "REFUND", "SUCCESSFUL"]
    try:
        if status not in statuses:
            raise Exception(f"Invalid status: {status}. Valid statuses are: {', '.join(statuses)}")

        base_url = "https://dev.api.oy-gul.uz/api/transaction/orders"
        params = {
            "page": page if page is not None else 1,
            "limit": limit if limit is not None else 20,
            "transactionStatus": status,
        }
        headers = {"Authorization": f"Bearer {tool_context.state['bearer_token']}"}
        timeout = 10
        response = requests.get(url=base_url, headers=headers, timeout=timeout, params=params)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Failed to get orders: {str(e)}",
        }


def confirm_order(order_id: str, tool_context: ToolContext) -> dict[str, Any] | None:
    """Confirms an existing order in the OyGul transaction service.

    This tool should be used when an order needs to be moved to the 'CONFIRMED'
    status, typically after payment has been verified or other confirmation
    criteria have been met.

    Args:
        order_id (str) required:
            The unique identifier of the order to be confirmed.
            Example: "8f38db18-0930-4fa4-8e75-a5fe7a552475"

    Returns:
        dict: The parsed JSON response from the API, confirming the order's new status.
        dict: An error dictionary if the request fails.

    Raises:
        requests.RequestException: If the HTTP request fails.
    """
    print("FUCKING ORDER ID", order_id)
    base_url = "https://dev.api.oy-gul.uz/api/transaction/orders/confirm"
    params = {"orderId": order_id.strip()}
    timeout = 10
    headers = {"Authorization": f"Bearer {tool_context.state['bearer_token']}"}

    try:
        response = requests.patch(url=base_url, params=params, headers=headers, timeout=timeout)
        response.raise_for_status()
        print(response.status_code)
        return response.json()
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Failed to confirm order: {str(e)}",
        }


def cancel_order(order_id: str, tool_context: ToolContext) -> dict[str, Any] | None:
    """Cancels an existing order in the OyGul transaction service.

    This tool should be used to cancel an order that is no longer required or
    cannot be fulfilled. It moves the order to a 'CANCELED' status. So order's current status should be a 'PENDING' to cancel;

    Args:
        order_id (str):
            The unique identifier of the order to be canceled.
            Example: "8f38db18-0930-4fa4-8e75-a5fe7a552475"

    Returns:
        dict: The parsed JSON response from the API, confirming the order's cancellation.
        dict: An error dictionary if the request fails.

    Raises:
        requests.RequestException: If the HTTP request fails.
    """
    base_url = "https://dev.api.oy-gul.uz/api/transaction/orders/cancel/" + order_id
    headers = {"Authorization": f"Bearer {tool_context.state['bearer_token']}"}
    timeout = 10

    try:
        response = requests.patch(url=base_url, headers=headers, timeout=timeout)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Failed to cancel order: {str(e)}",
        }
