from dataclasses import dataclass
from datetime import datetime

@dataclass
class Tick:
    timestamp: datetime
    price: float 
    quantity: int

    def __str__(self):
        return f'{self.timestamp},{self.price},{self.quantity}'
