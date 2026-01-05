class CleanResponseOutput:
    
    def __init__(self):
        return

    def safe_decode(self,value):
        if value is None:
            return ""
        if isinstance(value, bytes):
            return value.decode("utf-8", errors="replace")
        return str(value)