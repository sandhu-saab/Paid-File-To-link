from shortzy import Shortzy
from info import SHORTLINK_URL, SHORTLINK_API
import json
from datetime import datetime

class temp(object):
    ME = None
    BOT = None
    U_NAME = None
    B_NAME = None

async def get_shortlink(link):
    shortzy = Shortzy(api_key=SHORTLINK_API, base_site=SHORTLINK_URL)
    link = await shortzy.convert(link)
    return link

# ✅ Premium check function
def is_premium(user_id):
    try:
        with open("premium_users.json", "r") as f:
            data = json.load(f)
        expiry = data.get(str(user_id))
        if not expiry:
            return False
        expiry_date = datetime.strptime(expiry, "%Y-%m-%d")
        return expiry_date >= datetime.now()
    except:
        return False
