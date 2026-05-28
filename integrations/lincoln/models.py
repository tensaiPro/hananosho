from dataclasses import dataclass
from typing import Optional


@dataclass
class Reservation:

    reserve_no: str

    status: str

    receive_dt: str
    checkin: str
    raw: dict
    
    checkout: Optional[str] = None

    food_rank: Optional[str] = None

    guests: Optional[int] = None

    reserve_type: Optional[str] = None



    def same_as(self, other: dict):

        return (
            self.reserve_no == other.get("予約番号") and
            self.status == other.get("予約区分") and
            self.receive_dt == other.get("受信日時")
        )
