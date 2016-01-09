from pandas import Panel
import pandas as pd


class Market:
    """
    A set of TF2 items is represented as a `pandas` `Panel` object demarcating their combined historical cost table.
    """

    history = Panel()

    def __repr__(self):
        return str(self.history)

    def __init__(self, list_of_items):
        dict_of_frames = {item.name: item.history for item in list_of_items}
        self.history = pd.Panel.from_dict(dict_of_frames)
