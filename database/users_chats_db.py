import re
import motor.motor_asyncio
from info import DATABASE_NAME, DATABASE_URI

class Database:

    def __init__(self, uri, database_name):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(uri)
        self.db = self._client[database_name]
        self.col = self.db.users

    def new_user(self, id, name):
        return dict(
            id=id,
            name=name,
            last_use=None  # 🟡 Track last usage date
        )
    
    async def add_user(self, id, name):
        user = self.new_user(id, name)
        await self.col.insert_one(user)
    
    async def is_user_exist(self, id):
        user = await self.col.find_one({'id': int(id)})
        return bool(user)
    
    async def total_users_count(self):
        count = await self.col.count_documents({})
        return count

    async def get_all_users(self):
        return self.col.find({})

    async def delete_user(self, user_id):
        await self.col.delete_many({'id': int(user_id)})

    # ✅ Functions for daily access limit for free users
    async def get_last_use(self, user_id):
        data = await self.col.find_one({'id': int(user_id)})
        return data.get("last_use") if data else None

    async def set_last_use(self, user_id, date_str):
        await self.col.update_one({'id': int(user_id)}, {'$set': {'last_use': date_str}}, upsert=True)

db = Database(DATABASE_URI, DATABASE_NAME)
