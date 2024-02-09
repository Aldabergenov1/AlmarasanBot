from enum import Enum
from datetime import datetime


class Weekday(Enum):
    MONDAY = 1
    TUESDAY = 2
    WEDNESDAY = 3
    THURSDAY = 4
    FRIDAY = 5
    SATURDAY = 6
    SUNDAY = 7


class Container:
    def __init__(self, owner, week_day):
        self.owner = owner
        self.week_day = week_day
        self.created_at = datetime.now()
