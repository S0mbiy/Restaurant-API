from RestaurantType import RestaurantType
class User(RestaurantType):
    def __init__(self, user, password):
        super().__init__()
        self.user = user
        self.password = password



