import motor.motor_asyncio
import json


class Database:
    def __init__(self):
        with open("./config.json") as f:
            config = json.load(f)
        self.mongodb_uri = config["mongodb_uri"]

        self.cluster = motor.motor_asyncio.AsyncIOMotorClient(self.mongodb_uri)
        self.db = self.cluster["ShopBot"]
        self.levelling = self.db["levelling"]
        self.damage_contribution = self.db["damage_contribution"]
        self.economy = self.db["economy"]
        self.shop = self.db["shop"]
        self.item = self.db["item"]
        self.up = self.db["up"]


class ShopDB:
    def __init__(self, db):
        self.db = db
        self.shopdb = self.db.shop

    def template(self, d_id: int, shops: list = [], inventory: list = []):
        {
            "_id": d_id,
            "shops": {shop["name"]: shop for shop in shops},
            "inventory": inventory,
        }

    async def get_doc(self, d_id):
        return await self.shopdb.find_one({"_id": d_id})

    async def new_doc(self, d_id, shops: list = [], inventory: list = []):
        await self.shopdb.insert_one(self.template(d_id, shops, inventory))

    async def update_shops(self, d_id, shops: list):
        for shop in shops:
            await self.shopdb.update_one(
                {"_id": d_id}, {"$set": {"shop." + shop["name"]: shop}}
            )

    async def get_shops(self, d_id):
        doc = await self.get_doc(d_id)
        return doc.get("shops") if doc else None
