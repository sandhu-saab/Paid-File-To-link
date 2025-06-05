import json
from datetime import datetime, timedelta

PREMIUM_FILE = "premium_users.json"

def load_premium():
    try:
        with open(PREMIUM_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_premium(data):
    with open(PREMIUM_FILE, "w") as f:
        json.dump(data, f, indent=4)

def is_premium(user_id):
    users = load_premium()
    exp = users.get(str(user_id))
    if exp:
        return datetime.strptime(exp, "%Y-%m-%d") >= datetime.now()
    return False

def get_expiry(user_id):
    users = load_premium()
    return users.get(str(user_id))

def add_premium(user_id, days):
    users = load_premium()
    new_exp = (datetime.now() + timedelta(days=days)).strftime("%Y-%m-%d")
    users[str(user_id)] = new_exp
    save_premium(users)
