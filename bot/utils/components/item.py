import time


class Item:
    def __init__(self, name:str, description:str, price:float ,icon:str,sales:int=0):
        self.name = name.strip()
        self.description = description
        self.price = price # stays same
        self.value = price # value changes over time
        self.icon = icon
        self.release_time = time.time()

    
    def current_value(self):
        return self.value
    
    def to_dict(self):
        return {
            "name":self.name,
            "description":self.description,
            "price":self.price,
            "value":self.value,
            "icon":self.icon,
            "release_time":self.release_time
        }
    
    def from_dict(self,dat:dict):
        self.name = dat["name"]
        self.description = dat["description"]
        self.price = dat["price"]
        self.value = dat["value"]
        self.icon = dat["icon"]
        self.release_time = dat["release_time"]
        return self