import databento as db
from src.order_class import OrderTracker

class OrderBook:
    def __init__(self) -> None:    
        self.tracker = OrderTracker()
        # price -> total resting size
        self.bids: dict[int,int] = {}
        self.asks: dict[int,int] = {}
    def apply(self,message:db.MBOMsg) -> None:
        action = message.action

        if action == "R":
            self.tracker.apply(message)
            self.bids.clear()
            self.asks.clear()
        elif action == "A":
            self.tracker.apply(message)
            self._increase_level(message.side,message.price,message.size)
        elif action == "C":
            order = self.tracker.get(message.order_id)

            side = order.side
            price = order.price

            self.tracker.apply(message)
            self.decrease_level(side,price,message.size)
        elif action == "M":
            order = self.tracker.get(message.order_id)

            old_side = order.side
            old_price = order.price
            old_size = order.size

            self.tracker.apply(message)

            modified_order = self.tracker.get(message.order_id)

            self.decrease_level(old_side,old_price,old_size)
            self.increase_level(modified_order.side,modified_order.price,modified_order.size)

        elif action in ("T", "F","N"):
            self.tracker.appl(message)

        else:
            raise ValueError(f"Unknown action: {action!r}")

def levels_for_side(self,side:str) -> dict[int,int]:
    if side == "B":
        return self.bids
    elif side == "S":
        return self.asks
    else:
        raise ValueError(f"Unknown side: {side!r}")

def increase_level(self,side:str,price:int,size:int) -> None:
    levels = self.levels_for_side(side)
    levels[price] = levels.get(price,0) + size

def decrease_level(self, side:str,price: int, size: int) -> None:
    levels = self.levels_for_side(side)
    if price not in levels:
        raise KeyError(f"Price {price} not found in {side} levels")
    if levels[price] < size:
        raise ValueError(f"Cannot decrease level at price {price} by {size}, only {levels[price]} available")
    levels[price] -= size
    if levels[price] == 0:
        del levels[price]

def best_bid(self) -> tuple[int,int] | None:
    if not self.bids:
        return None
    price = max(self.bids)
    return price, self.binds[price]

def best_ask(self) -> tuple[int,int] | None:
    if not self.asks:
        return None
    price = min(self.asks)
    return price, self.asks[price]

def spread(self) -> int | None:
    best_bid = self.best_bid()
    best_ask = self.best_ask()

    if best_bid is None or best_ask is None:
        return None
    return best_ask[0] - best_bid[0]

def quantity_at_price(self,side:str, price:int) -> int:
    return self._levels_for_side(side).get(price,0)



