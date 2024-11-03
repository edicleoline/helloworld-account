from __future__ import annotations

from enum import Enum

class VerificationType(Enum):
    PHONE = "phone"
    DEVICE = "device"
    EMAIL = "email"

    @classmethod
    def from_string(cls, value: str) -> VerificationType:
        try:
            return cls[value.upper()]
        except KeyError:
            raise ValueError(f"'{value}' is not a valid VerificationType")