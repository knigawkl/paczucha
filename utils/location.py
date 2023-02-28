"""The module contains the Location dataclass."""
from dataclasses import dataclass

@dataclass
class Location:
    """Represents a real-world location.

    Attributes:
        latitude: You know latitude from geography lessons.
        longitude: You know longitude from geography lessons.
        radius: Location radius in kilometers.

    """
    latitude: float
    longitude: float
    radius: int
