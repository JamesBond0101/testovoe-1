class PriceNotFoundException(Exception):
    """Raised when a price is not found"""


class InvalidPriceDateRangeException(Exception):
    """Raised when date_from is greater than date_to."""