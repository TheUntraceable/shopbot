import io

import discord
from PIL import Image


class ImageGen:
    def gen(self, conf: dict):
        get = lambda x: conf.get(x)
        if get("world"):
            world = Image.open(f"./assets/shop/world/{conf['world']}.png")
        world = world.resize((512, 512))
        if get("top"):
            top = Image.open(f"./assets/shop/top/{conf['top']}.png")
            top = top.resize((512, 512))
            world.paste(top, (0, 0), top)
        if get("wall"):
            wall = Image.open(f"./assets/shop/wall/{conf['wall']}.png")
            wall = wall.resize((512, 512))
            world.paste(wall, (0, 0), wall)
        if get("door"):
            door = Image.open(f"./assets/shop/door/{conf['door']}.png")
            door = door.resize((512, 512))
            world.paste(door, (0, 0), door)
        if get("roof"):
            roof = Image.open(f"./assets/shop/roof/{conf['roof']}.png")
            roof = roof.resize((512, 512))
            world.paste(roof, (0, 0), roof)
        arr = io.BytesIO()
        path = f"./image/{get('world')}-{get('wall')}-{get('roof')}-{get('top')}-{get('door')}.png"
        world.save(arr, format="PNG")
        arr.seek(0)
        f = discord.File(arr, filename=path.split("/")[-1])
        return f,path.split("/")[-1]
