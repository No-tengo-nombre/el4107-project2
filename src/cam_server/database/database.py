import base64
import datetime
import hashlib
import json
import threading
import uuid

from cam_server.database.constants import USER_DATABASE_FILE

from cam_common.logger import LOGGER


def _encrypt(password, salt):
    t_sha = hashlib.sha512()
    t_sha.update((password + salt).encode())
    return base64.urlsafe_b64encode(t_sha.digest())


class UserNotFoundException(Exception):
    """Exception when a user is not found."""

    def __init__(self, username) -> None:
        super().__init__(f"User {username} was not found.")


class UserAlreadyExistsException(Exception):
    """Exception when a user already exists."""

    def __init__(self, username) -> None:
        super().__init__(f"User {username} already exists.")


class DateTimeEncoderDecoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime.date, datetime.datetime)):
            return obj.isoformat()

    @staticmethod
    def decode(json_dict):
        if "users" in json_dict:
            for user, features in json_dict["users"].items():
                json_dict["users"][user]["join_date"] = datetime.datetime.fromisoformat(
                    features["join_date"]
                )
        return json_dict


class __UserDatabase:
    db_file = USER_DATABASE_FILE
    mutex = threading.Lock()

    def __init__(self) -> None:
        self._update_db()

    def _update_db(self):
        with open(self.db_file, "r") as file:
            self.db = json.load(file, object_hook=DateTimeEncoderDecoder.decode)

    def user_exists(self, username):
        user = self.db["users"].get(username)
        return user

    def validate_user(self, username, password):
        LOGGER.info("Validating user")
        with self.mutex:
            self._update_db()
            user = self.user_exists(username)
            if user is not None:
                LOGGER.info("Found user")
                user_salt = user["salt"]
                return _encrypt(password, user_salt) == user["password"].encode()
            else:
                raise UserNotFoundException(username)

    def save_db_file(self, db):
        LOGGER.info("Saving database file")
        with open(self.db_file, "w") as file:
            json.dump(db, file, indent=2, cls=DateTimeEncoderDecoder)

    def register_user(self, username, password):
        LOGGER.info("Registering user")
        with self.mutex:
            self._update_db()
            if self.user_exists(username) is not None:
                raise UserAlreadyExistsException(username)
            else:
                salt = str(uuid.uuid4())
                self.db["users"][username] = {
                    "salt": salt,
                    "password": _encrypt(password, salt).decode(),
                    "join_date": datetime.datetime.now(),
                }
                self.save_db_file(self.db)


USER_DATABASE = __UserDatabase()
