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
    
    def add(self, message:db.MBOMsg) -> None:
        if message.order_id==0:
            raise ValueError("Order ID cannot be zero.")
        if message.order_id in self.orders:
            raise ValueError(f"DUPLICATION ERROR: Order ID {message.order_id} already exists.")
        if message.side not in ("A","B"):
            raise ValueError(f"Invalid side: {message.side}. Must be 'A' (ask) or 'B' (bid).")
        if message.size <= 0: 
            raise ValueError(f"Invalid size: {message.size}. Must be greater than zero.")
        order = Order(
            order_id=message.order_id,
            price=message.price,
            quantity=message.quantity,
            side=message.side,
            size=message.size,
            timestamp=message.timestamp,
            ts_event=message.ts_event
        )
        self.orders[order.order_id] = order

    def cancel(self,message:db.MBOMsg) -> None:
        if message.order_id not in self.orders:
            f"cannot cancel order with ID {message.order_id} because it does not exist."
            raise ValueError(f"Order ID {message.order_id} does not exist.")
        order = self.orders[message.order_id]

        if message.size > order.size:
            raise ValueError(f"Cannot cancel {message.size} from order ID {message.order_id} because only {order.size} is available.")
        order.size -= message.size
        if order.size <= 0:
            del self.orders[message.order_id]
        def modify(self,message:db.MBOMsg) -> None:
            if message.order_id not in self.orders:
                raise ValueError(f"Order ID {message.order_id} does not exist.")
            order = self.orders[message.order_id]
            if message.price is not None:
                order.price = message.price
            if message.quantity is not None:
                order.quantity = message.quantity
            if message.size is not None:
                order.size = message.size
            if message.side is not None:
                order.side = message.side
            if message.timestamp is not None:
                order.timestamp = message.timestamp
            loses_priority = (message.price != order.price) or (message.size > order.size)
            order.price = message.price
            order.size = message.size
            if loses_priority:
                order.ts_event = message.ts_event      