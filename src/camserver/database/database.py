import json

from camserver.database.constants import USER_DATABASE_FILE


def user_exists(username):
    db = fetch_database()
    user = db["user"].get(username)
    return bool(user)


def fetch_database():
    with open(USER_DATABASE_FILE, "r") as db:
        return json.load(db)
