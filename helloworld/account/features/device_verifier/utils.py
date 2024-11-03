from __future__ import annotations

from datetime import datetime, timedelta
from typing import Optional

import pytz

def can_request_otp(last_request_at: Optional[datetime], cooldown_seconds: int) -> bool:
    if last_request_at is None:
        return True

    current_time = datetime.now(pytz.utc)
    allowed_time = last_request_at + timedelta(seconds=cooldown_seconds)

    return current_time >= allowed_time
