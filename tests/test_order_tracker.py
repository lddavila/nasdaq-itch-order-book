from types import SimpleNamespace
import pytest

from src.order_class import OrderTracker

def message(
        action: str,
        order_id: int =1,
        price: int = 100_000_000_000,
        size: int = 100,
        side: str = "B",
        priority_ts_event: int = 1_000):
    return SimpleNamespace(
        action=action,
        order_id=order_id,
        price=price,
        size=size,
        side=side,
        priority_ts_event=priority_ts_event,
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
    tracker.apply(message("C",size=40,priority_ts_event=2_000))

    assert tracker.get(1).size==60

    #modify price and size
    tracker.apply(
        message(
            "M",
            price=101_000_000_000,
            size=80,
            priority_ts_event=3_000 
        )
    )

    order = tracker.get(1)
    assert order.price==101_000_000_000
    assert order.size==80   
    assert order.priority_ts_event==3_000

    #cancel the remaining quantity
    tracker.apply(message("C",size=80,priority_ts_event=4_000))
    assert len(tracker)==0
    assert 1 not in tracker

def test_duplicate_order_is_rejected():
    tracker = OrderTracker()

    tracker.apply(message("A"))

    with pytest.raises(ValueError, match="DUPLICATION ERROR: Order ID 1 already exists."):
        tracker.apply(message("A"))

def test_unknown_cancellation_is_rejected():
    tracker = OrderTracker()
    with pytest.raises(ValueError, match=f"Order ID 999 does not exist."):
        tracker.apply(message("C",order_id=999,size=10))

def test_over_cancelation_is_rejected():
    tracker = OrderTracker()
    tracker.apply(message("A",size=100))
    with pytest.raises(ValueError, match="Cannot cancel 101 from order ID 1 because only 100 is available."):
        tracker.apply(message("C",size=101))

def test_clear_removes_all_orders():
    tracker = OrderTracker()
    tracker.apply(message("A",order_id=1))
    tracker.apply(message("A",order_id=2,side="A"))
    assert len(tracker)==2
    tracker.apply(message("R"))
    assert len(tracker)==0

@pytest.mark.parametrize("action",["T","F","N"])
def test_unknown_book_actions_are_ignored(action):
    tracker = OrderTracker()
    tracker.apply(message(action))
    assert len(tracker)==0
