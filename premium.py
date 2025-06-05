import json
import os
from datetime import datetime, timedelta

# 🔸 File to store premium user data
DB_FILE = "premium_users.json"

# 🔸 Load premium users
def load_db():
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, "w") as f:
            json.dump({}, f)
    with open(DB_FILE, "r") as f:
        return json.load(f)

# 🔸 Save premium users
def save_db(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f)

# 🔸 Add or update premium user
def set_premium(user_id: int, days: int):
    data = load_db()
    expiry = datetime.now() + timedelta(days=days)
    data[str(user_id)] = expiry.strftime("%Y-%m-%d")
    save_db(data)

# 🔸 Check if user is premium
def is_premium(user_id: int) -> bool:
    data = load_db()
    exp_str = data.get(str(user_id))
    if exp_str:
        expiry = datetime.strptime(exp_str, "%Y-%m-%d")
        return expiry >= datetime.now()
    return False

# 🔸 Get premium expiry date
def get_expiry(user_id: int) -> str:
    data = load_db()
    return data.get(str(user_id), "No active plan")
