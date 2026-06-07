from dataclasses import dataclass
from typing import Optional


@dataclass
class Subscription:
    id: int
    name: str
    print: int
    paid: bool = False
    payment_date: Optional[str] = None

    