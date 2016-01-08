from pandas import Panel


class Market:
    """
    A set of TF2 items is represented as a `pandas` `Panel` object demarcating their combined historical cost table.
    """

    history = Panel()

    def __repr__(self):
        return str(self.history)

    def __init__(self, dict_of_items):
        # dict_of_frames = dict((name, item.history) for (name, item) in dict_of_items)
        self.history = Panel(dict_of_frames)