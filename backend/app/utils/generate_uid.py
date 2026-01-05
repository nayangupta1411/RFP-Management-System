import uuid
class GenerateUID:  
    def __init__(self):
        self.uid=None
        
    def unique_uid(self,length=8):
        unique_id=str(uuid.uuid4().hex[:length])
        print(f'unique_id : {unique_id}')
        self.uid=unique_id
        return self.uid