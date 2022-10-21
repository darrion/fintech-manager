from enum import Enum 

INTEGER_PRECISION = 12
DECIMAL_PRECISION = 2

class AccountType(Enum):

    BROKERAGE = "brokerage"
    IRA = "ira"
