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
            