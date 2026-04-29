from enum import Enum

class OrderStatus(str, Enum):
    PLACED = "PLACED"
    PACKED = "PACKED"
    SHIPPED = "SHIPPED"
    DELIVERED = "DELIVERED"

VALID_STATUS_FLOW = {
    "PLACED": ["PACKED"],
    "PACKED": ["SHIPPED"],
    "SHIPPED": ["DELIVERED"],
    "DELIVERED": []
}