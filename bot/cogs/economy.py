from random import randint
from typing import Optional
from discord import Embed, User
from discord.ext import commands


class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def get_default_document(self, author_id):
        return {
            "user_id": author_id,
            "wallet": 0,
            "bank": 0,
            "max_bank": 0,
            "daily_streak": 0,
        }

    @commands.command(aliases=["b", "bal"])
    async def balance(self, ctx, member: Optional[User] = None):
        """Check your balance."""
        member = member or ctx.author
        document = await self.bot.db.economy.find_one({"user_id": member.id})

        if document is None:
            await self.bot.db.economy.insert_one(self.get_default_document(member.id))
            document = self.get_default_document(member.id)

        embed = Embed(
            title=f"{member}'s balance",
        )

        embed.add_field(name="Wallet", value=document["wallet"])
        embed.add_field(name="Bank", value=document["bank"])
        embed.add_field(name="Max Bank", value=document["max_bank"])
        embed.add_field(name="Daily Streak", value=document["daily_streak"])
        embed.set_footer(text=str(ctx.author))
        await ctx.reply(embed=embed)

    @commands.command(aliases=["w"])
    async def withdraw(self, ctx, amount: int):
        """Withdraw money from your bank"""
        document = await self.bot.db.economy.find_one({"user_id": ctx.author.id})
        if document is None:
            await self.bot.db.economy.insert_one(
                self.get_default_document(ctx.author.id)
            )
            document = self.get_default_document(ctx.author.id)
        if document["bank"] < amount:
            await ctx.reply("You don't have that much in your bank.")
            return
        await self.bot.db.economy.update_one(
            {"user_id": ctx.author.id},
            {"$inc": {"bank": -amount, "wallet": amount}},
        )
        await ctx.reply(f"You withdrew {amount} from your bank.")

    @commands.command(aliases=["dep"])
    async def deposit(self, ctx, amount: int):
        """Deposit money into your bank"""
        document = await self.bot.db.economy.find_one({"user_id": ctx.author.id})
        if document is None:
            await self.bot.db.economy.insert_one(
                self.get_default_document(ctx.author.id)
            )
            document = self.get_default_document(ctx.author.id)
        if document["wallet"] < amount:
            await ctx.reply("You don't have that much in your wallet.")
            return

        if sum(document["bank"], amount) > document["max_bank"]:
            await ctx.reply("You can't deposit that much in your bank.")
            return

        await self.bot.db.economy.update_one(
            {"user_id": ctx.author.id},
            {"$inc": {"wallet": -amount, "bank": amount}},
        )
        await ctx.reply(f"You deposited {amount} into your bank.")

    @commands.Cog.listener()
    async def on_command_completion(self, ctx):
        await self.bot.db.economy.update_one(
            {"user_id": ctx.author.id}, {"$inc": {"max_bank": randint(1, 50)}}
        )

    def calculate_shop_income(self, shop):
        return sum(item["price"] for item in shop["items"]) * shop["level"]

    @commands.command(aliases=["d"])
    async def collect(self, ctx):
        """Get your daily reward"""
        document = await self.bot.db.economy.find_one({"user_id": ctx.author.id})
        if document is None:
            await self.bot.db.economy.insert_one(
                self.get_default_document(ctx.author.id)
            )
            document = self.get_default_document(ctx.author.id)
        shop = await self.bot.db.shop.find_one({"user_id": ctx.author.id})
        if shop is None:
            await ctx.reply("you dont have a shop to collect income from")
            return
        amount = self.calculate_shop_income(shop)
        while document["daily_streak"] > 0:
            amount *= 1.1
            document["daily_streak"] -= 1
        await self.bot.db.economy.update_one(
            {"user_id": ctx.author.id},
            {"$inc": {"wallet": amount, "daily_streak": 1}},
        )
        await ctx.reply(f"You claimed your daily reward and got {amount}!")
