from item import Item
from item import get_all_items
# import time


# This loop instantiates all non-unusual Items in the game: and thus saves them to local CSV files.
# NOTE: This script takes a very long time to run as it has to generate over 3500 requests.

for item in get_all_items():
    quality = item.split(" ")[0]
    craftability = item.split(" ")[1]
    tradability = item.split(" ")[2]
    name = " ".join(item.split(" ")[3:])
    Item(name, quality=quality, craftability=craftability, tradability=tradability)
