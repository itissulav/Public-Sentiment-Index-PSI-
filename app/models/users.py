class User:
    def __init__(self):
        self._user_id = None
        self._first_name = None
        self._last_name = None
        self._email = None
        self._username = None
        self._password = None
        self._role = None

    # ---------- Constructors ----------

    @classmethod
    def login_user(cls, username, password):
        user = cls()
        user.set_username(username)
        user.set_password(password)
        return user
    
    @classmethod
    def login_user_email(cls, email, password):
        user = cls()
        user.set_email(email)
        user.set_password(password)
        return user

    @classmethod
    def register_user(cls, first_name, last_name, email, username, password):
        user = cls()
        user.set_first_name(first_name)
        user.set_last_name(last_name)
        user.set_email(email)
        user.set_username(username)
        user.set_password(password)
        return user

    # ---------- Getters ----------
    def get_user_id(self):
        return self._user_id

    def get_first_name(self):
        return self._first_name

    def get_last_name(self):
        return self._last_name

    def get_email(self):
        return self._email

    def get_username(self):
        return self._username

    def get_password(self):
        return self._password
    
    def get_role(self):
        return self._role

    # ---------- Setters ----------
    def set_user_id(self, user_id):
        self._user_id = user_id

    def set_first_name(self, first_name):
        self._first_name = first_name

    def set_last_name(self, last_name):
        self._last_name = last_name

    def set_email(self, email):
        self._email = email

    def set_username(self, username):
        self._username = username

    def set_password(self, password):
        self._password = password
    
    def set_role(self, role):
        self._role = role

    # ---------- Utility ----------

    def to_dict(self):
        return {
            "user_id": self._user_id,
            "first_name": self._first_name,
            "last_name": self._last_name,
            "email": self._email,
            "username": self._username,
            "password": self._password,
            "role": self._role
        }

    @staticmethod
    def from_dict(data):
        user = User()
        user.set_user_id(data.get("user_id"))
        user.set_first_name(data.get("first_name"))
        user.set_last_name(data.get("last_name"))
        user.set_email(data.get("email"))
        user.set_username(data.get("username"))
        user.set_password(data.get("password"))
        user.set_role(data.get("role"))
        return user