
from src.order_book import OrderBook
from types import SimpleNamespace

def message(action: str,order_id: int=1,price: int=100_000_000_000,size: int = 100, side: str = "B", priority_ts_event: int = 1_000):
    return SimpleNamespace(action=action, order_id=order_id, price=price, size=size, side=side, priority_ts_event=priority_ts_event)

def test_orders_at_same_price_are_aggregated():
    book = OrderBook()

    book.apply(message("A",order_id=1,side="B",price=100_000_000_000,size=100))
    book.apply(message("A",order_id=2,side="B",price=100_000_000_000,size=50))

    assert book.best_bid() == (100_000_000_000, 150)
    assert book.quantity_at_price("B",100_000_000_000) == 150

    assert len(book.tracker) == 2
    assert book.tracker.get(1).size == 100
    assert book.tracker.get(2).size == 50
