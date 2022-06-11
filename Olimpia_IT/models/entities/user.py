from werkzeug.security import check_password_hash

class User():

    def __init__(self, username, password):
        self.username = username
        self.password = password

    @classmethod
    def check_password(self, hashed_password, password):
        return check_password_hash(hashed_password, password)
