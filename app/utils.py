from datetime import datetime, timedelta, timezone

def to_local(dt):
    if dt is None:
        return None
    # 新加坡/台灣時區 UTC+8
    local_tz = timezone(timedelta(hours=8))
    return dt.astimezone(local_tz)
