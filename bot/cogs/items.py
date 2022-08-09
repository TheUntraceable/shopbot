from discord.ext import commands
import discord
import random


class Items(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def template(self, msg, name, desc):
        return {
            "_id": msg.author.id,
            "name": name,
            "description": desc,
            "stock": 10,
            "max_stock": 10,
            "price": 1,
            "sold": 0,
        }

    @commands.group(name="item", invoke_without_command=True)
    async def item(self, ctx):
        await ctx.send("Use `!item <item>` to get info on an item.")

    @item.command(name="new", aliases=["create", "make"])
    async def item_new(self, ctx):
        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel

        async def do_prompt():
            await ctx.send(
                "What would you like to name your item?(can also be an emoji)[ max_words=1 , max_len=10 ]"
            )
            return await self.bot.wait_for("message", check=check)

        async def do_prompt_desc():
            await ctx.send(
                "give a description of your item [ max_words=15 , max_len=150 ]"
            )
            return await self.bot.wait_for("message", check=check)

        for _ in range(5):
            msg = await do_prompt()
            cont = msg.content.lower().strip()
            dcont = None
            if len(cont.split()) == 1 and len(cont) <= 10:
                for _ in range(5):
                    dmsg = await do_prompt_desc()
                    dcont = dmsg.content.lower().strip()
                    if len(dcont.split()) <= 15 and len(dcont) <= 150:
                        break
                    dcont = None
                    await ctx.send("invalid description")
                else:
                    await ctx.reply("you failed to create a description")
                    break
                if dcont:
                    await self.bot.db.item.insert_one(self.template(msg, cont, dcont))
                    await ctx.send("item created")
                    break
            await ctx.send("invalid name")
        else:
            await ctx.reply("you failed to create an item")

    @item.command(name="restock")
    async def item_restock(self, ctx):
        shop = await self.bot.db.shop.find_one({"_id": ctx.author.id})
        if not shop:
            await ctx.send("You don't have a shop.")
            return
        await ctx.send("restocking")
        max_inc = random.randint(0, 5)
        stock_inc = random.randint(1, max_inc if max_inc != 0 else 1)
        await self.bot.db.item.update_one(
            {"_id": ctx.author.id}, {"$inc": {"max_stock": max_inc}}
        )
        await self.bot.db.item.update_one(
            {"_id": ctx.author.id}, {"$set": {"stock": stock_inc}}
        )
        await ctx.send(
            f"restocked {stock_inc}items and max stock increased by {max_inc}"
        )


async def setup(bot):
    await bot.add_cog(Items(bot))
