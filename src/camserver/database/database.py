import json
import hashlib
import base64

from camserver.database.constants import USER_DATABASE_FILE


def __encrypt(password, salt):
    t_sha = hashlib.sha512()
    t_sha.update((password + str(salt)).encode())
    return base64.urlsafe_b64encode(t_sha.digest())


class UserNotFoundException(Exception):
    """Exception when a user is not found."""
    def __init__(self, username) -> None:
        super().__init__(f"User {username} was not found.")


class UserDatabase:
    db_file = USER_DATABASE_FILE

    def __init__(self) -> None:
        with open(UserDatabase.db_file, "r") as db:
            self.db = json.load(db)

    def user_exists(self, username):
        user = self.db["users"].get(username)
        return user

    def validate_user(self, username, password):
        user = self.user_exists(username)
        if user is not None:
            user_salt = user["salt"]
            return __encrypt(password, user_salt) == user["password"]
        else:
            raise UserNotFoundException(username)
