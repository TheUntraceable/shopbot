class Shop:
    def __init__(
        self,
        name: str,
        icon: str,
        price: float,
        description: str,
        shop_dat: dict,
        inventory: list,
    ):
        self.name = name
        self.icon = icon
        self.price = price
        self.description = description
        self.shop_dat = shop_dat
        self.inventory = inventory

    def new(
        name: str,
        icon: str,
        price: int,
        description: str,
        shop_dat: dict = None,
        inventory: list = None,
    ) -> "Shop":
        def_shop_dat = {"top": "def", "roof": "def", "wall": "def", "door": "def"}
        return super().__init__(
            name,
            icon,
            price,
            description,
            shop_dat if shop_dat else def_shop_dat,
            inventory if inventory else [],
        )

    def restock(self, multiplier: int = 1, item: str = None):
        ...

    def to_dict(self):
        return {
            "name": self.name,
            "icon": self.icon,
            "price": self.price,
            "description": self.description,
            "shop_dat": self.shop_dat,
            "inventory": self.inventory,
        }

    def from_dict(self, shop_dat: dict):
        self.name = shop_dat["name"]
        self.icon = shop_dat["icon"]
        self.price = shop_dat["price"]
        self.description = shop_dat["description"]
        self.shop_dat = shop_dat["shop_dat"]
        self.inventory = shop_dat["inventory"]
        return self

    def update(self, shop_dat: dict):
        self.shop_dat.update(shop_dat)
        return self

    async def render_shop(self):
        # render an image of the shop with the components~
        return self.to_dict()
