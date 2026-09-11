
from src.order_book import OrderBook
from types import SimpleNamespace
import pytest

def message(action: str,order_id: int=1,price: int=100_000_000_000,size: int = 100, side: str = "B", ts_event: int = 1_000):
    return SimpleNamespace(action=action, order_id=order_id, price=price, size=size, side=side, ts_event=ts_event)

def test_orders_at_same_price_are_aggregated():
    book = OrderBook()

    book.apply(message("A",order_id=1,side="B",price=100_000_000_000,size=100))
    book.apply(message("A",order_id=2,side="B",price=100_000_000_000,size=50))

    assert book.best_bid() == (100_000_000_000, 150)
    assert book.quantity_at_price("B",100_000_000_000) == 150

    assert len(book.tracker) == 2
    assert book.tracker.get(1).size == 100
    assert book.tracker.get(2).size == 50

def test_modify_moves_order_to_new_price():
    book = OrderBook()
    book.apply(message("A",order_id=1,side="B",price=100_000_000_000,size=100))
    book.apply(message("M",order_id=1,side="B",price=101_000_000_000,size=80,ts_event=2000))
    assert book.quantity_at_price("B",100_000_000_000) == 0
    assert book.quantity_at_price("B",101_000_000_000) == 80
    assert book.best_bid() == (101_000_000_000, 80)

    assert book.tracker.get(1).price == 101_000_000_000
    assert book.tracker.get(1).size == 80

def test_valid_book_passes_validation():
    book = OrderBook()
    book.apply(message("A",order_id=1,side="B",price=100_000_000_000,size=100))
    book.apply(message("A",order_id=2,side="A",price=100_000_000_000,size=50))
    book.apply(message("A",order_id=3,side="A",price=101_000_000_000,size=80))
    book.validate()

def test_validation_detects_incorrect_bid_quantity():
    book = OrderBook()
    book.apply(message("A",order_id=1,side="B",price=100_000_000_000,size=100))
    book.apply(message("A",order_id=2,side="B",price=100_000_000_000,size=50))
    # Manually tamper with the bids to create an inconsistency
    book.bids[100_000_000_000] = 200  # Should be 150
    with pytest.raises(ValueError, match="Bids do not match expected levels. Expected: {100000000000: 150}, Actual: {100000000000: 200}"):
        book.validate()

def test_validation_detects_untracked_price_level():
    book = OrderBook()

    #create a price level without an underlying order
    book.asks[101_000_000_000] = 50
    with pytest.raises(ValueError,match="Asks do not match expected levels. Expected: {}, Actual: {101000000000: 50}"):
        book.validate()