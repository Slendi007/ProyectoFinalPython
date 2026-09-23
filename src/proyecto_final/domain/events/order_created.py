from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class OrderCreated:
    order_id: int
    customer: str
    occurred_at: datetime
