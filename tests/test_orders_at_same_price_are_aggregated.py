
from src.order_book import OrderBook
import pytest
import databento as db

def test_orders_at_same_price_are_aggregated():
    book = OrderBook()

    book.apply(message("A",order_id=1,side="B",price=100_000_000_000,size=100))
    book.apply(message("A",order_id=2,side="B",price=100_000_000_000,size=50))

    assert book.best_bid() == (100_000_000_000, 150)