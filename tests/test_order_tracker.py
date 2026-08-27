from types import SimpleNamespace
import pytest

from src.order_class import OrderTracker

def message(
        action: str,
        order_id: int =1,
        price: int = 100,
        size: int = 100,
        side: str = "B",
        ts_event: int = 1_000):
    return SimpleNamespace(
        action=action,
        order_id=order_id,
        price=price,
        size=size,
        side=side,
        ts_event=ts_event
    )
def test_complete_order_lifecycle():
    tracker = OrderTracker()

    #add 100 shares at $100
    tracker.apply(message("A"))

    assert len(tracker)==1
    assert 1 in tracker

    order = tracker.get(1)

    assert order.order_id ==1
    assert order.price == 100_000_000_000
    assert order.size==100
    assert order.side=="B"
    assert order.priority_ts_event==1_000

    #partially cancel 40 shares
    tracker.apply(message("C",size=40,ts_event=2_000))

    assert tracker.get(1).size==60

    #modify price and size
    tracker.apply(
        message(
            "M",
            price=101_000_000_000,
            size=80,
            ts_event=3_000 
        )
    )

    order = tracker.get(1)
    assert order.price==101_000_000_000
    assert order.size==80   
    assert order.priority_ts_event==3_000

    #cancel the remaining quantity
    tracker.apply(message("C",size=80,ts_event=4_000))
    assert len(tracker)==0
    assert 1 not in tracker