from datetime import datetime, timezone
from zoneinfo import ZoneInfo

class DateTime:
    
    def __init__(self):
        self.time=None
        self.timezone=None
        
    def timezone(self):
        self.timezone=ZoneInfo("Asia/Kolkata")
        return self.timezone
    
    @staticmethod
    def time_utc():
        return datetime.now(timezone.utc)
    
    def utc_to_ist(self,dt):
        if dt.tzinfo is None:
            raise ValueError("Datetime must be timezone-aware")
        return dt.astimezone(self.timezone())
    
    def time_ist(self,dt):
        return self.utc_to_ist(dt).strftime("%d-%m-%Y %I:%M:%S %p")
        
        