from datetime import datetime
import uuid
class RestaurantType:
    def __init__(self, ID=None):
        if ID is None:
            self.ID = str(uuid.uuid4())[:8]
        else:
            self.ID = ID
        self.creation_date = str(datetime.now())
