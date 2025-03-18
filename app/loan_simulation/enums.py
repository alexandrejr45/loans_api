from decimal import Decimal
from enum import Enum

class InterestRateByAge(Enum):
    YOUNG = Decimal('0.05')
    ADULT = Decimal('0.03')
    OLD_ADULT = Decimal('0.02')
    ELDERLY = Decimal('0.04')
