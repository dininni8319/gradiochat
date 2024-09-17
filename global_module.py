# I am not using it for now
class Globals:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Globals, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        self.user_id = None
        self.token = None

    def set_user_id(self, user_id):
        self.user_id = user_id

    def set_token(self, token):
        self.token = token

    def get_user_id(self):
        return self.user_id

    def get_token(self):
        return self.token

# Create a global instance
global_instance = Globals()


