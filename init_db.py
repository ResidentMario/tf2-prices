import sqlite3
import os
from bs4 import BeautifulSoup
import requests
import urllib


def get_all_items():
    """
    Parses the backpack.tf item spreadsheet in order to retrieve every non-usual item in the game which is on the
    market.
    :return:
    """
    spreadsheet = BeautifulSoup(requests.get("http://backpack.tf/pricelist/spreadsheet").text, 'html.parser')
    item_strings = spreadsheet.find_all("a", {"class": 'qlink'})
    ret = []
    for (item_string, num) in zip(item_strings, range(len(item_strings))):
        item_string = str(item_string)
        repr = (
            urllib.request.unquote(item_string.split("/")[3]),
            urllib.request.unquote(item_string.split("/")[2]),
            item_string.split("/")[4],
            item_string.split("/")[5][:item_string.split("/")[5].find('"')],
            num
        )
        ret.append(repr)
    return ret


if __name__ == '__main__':
    conn = sqlite3.connect('tf2idb.sq3')
    c = conn.cursor()
    # if os.path.isfile('tf2_items.db'):
    #     print("Connecting to database...")
    # else:
    #     print("Initializing database...")
    # conn = sqlite3.connect('tf2_items.db')
    # c = conn.cursor()
    # # The following segment regenerates the Items data table, not necessary during development.
    # print("Resetting tables...")
    # c.execute('''DROP TABLE items''')
    # conn.commit()
    # # The following query fails the unique constraint test for reasons unknown.
    # # c.execute('''CREATE TABLE items
    # #   (name text, quality text, tradable integer, craftable integer, PRIMARY KEY (name, quality, tradable, craftable))
    # # ''')
    # c.execute('''CREATE TABLE items
    #   (name text, quality text, tradable integer, craftable integer, price_index integer PRIMARY KEY)
    # ''')
    # conn.commit()
    # print("Retrieving marketable items list...")
    # items_in = get_all_items()
    # print("Storing marketable items in database...")
    # c.executemany('INSERT INTO items VALUES (?,?,?,?,?)', items_in)
    # conn.commit()
    # for row in c.execute('SELECT * FROM items ORDER BY name'):
    #     print(row)
    conn.close()