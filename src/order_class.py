import databento as db
class Order:
    order_id: int
    price: float
    quantity: int
    side: str  # 'buy' or 'sell'
    size: int
    timestamp: int

class OrderTracker:
    def __init__(self) -> None:
        self.orders: dict[int, Order] = {}
    def apply(self,message: db.MBOMsg) -> None:
        action = message.action
        if message.action == "R":
            self.orders.clear()
        elif message.action == "A":
            self.add(message)
        elif message.action == "C":
            self.cancel_order(message)
        elif message.action == "M":
            self.modify(message)
        elif action in ("T", "F","N"):
            pass
        else:
            raise ValueError(f"Unknown action: {action}")