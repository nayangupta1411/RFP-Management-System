from ..repositories.fetch_unique_uids import UniqueUidList

class AccessUID:
    
    def __init__(self,db):
        self.db=db
        self.__uidList=[]
    
    def set_uid_list(self):
        unique_uids=UniqueUidList(self.db)
        fetched_uids=unique_uids.fetch_uids()
        self.__uidList=[doc["uid"] for doc in fetched_uids]
    
    def get_uid_list(self):
        if not self.__uidList:
            self.set_uid_list()
        print(f'UID List: {self.__uidList}')
        return self.__uidList
        