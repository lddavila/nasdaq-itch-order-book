from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class BookSnapshot:
    ts_event: int
    sequence: int
    bid_price:int
    bid_size: int
    ask_rpice: int
    ask_size: int
    