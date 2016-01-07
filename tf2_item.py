from pandas import Series, DataFrame
import pandas as pd
import numpy as np
import requests
import json
import arrow
import os

# TODO: Not working at all.


class Item:
    """
    Each TF2 item is represented as a `pandas` `DataFrame` object demarcating its historical cost table.
    """
    
    history = DataFrame()
    
    def __repr__(self):
        return str(self.history)

    def __init__(self, item, **kwargs):
        if len(item) > 0:
            # Make the API call.
            params = {"key": _get_key(), "item": item}
            params.update(kwargs)
            data = json.loads(requests.get("http://backpack.tf/api/IGetPriceHistory/v1/",
                                           params=params).text)['response']['history']
            # Parse it into a `pandas` `DataFrame`.
            frame = DataFrame(data,
                              index=[np.datetime64(str(arrow.get(t['timestamp']).format('YYYY-MM-DD'))) for t in data],
                              columns=["currency", "value", "value_high"])
            # Throw out earlier dates, for the moment. `2013-01-01` is the starting point for all knowledge.
            frame = frame[pd.to_datetime('2013-01-01'):]
            # Extrapolate Refined Metal price back to `2013-01-01`.
            if item == "Refined Metal":
                frame.loc[pd.to_datetime('2013-01-01')] = ['usd', 0.40, 0.40]
                frame = frame.sort_index()
            # Rebase rows from `2013-01-01` forward to USD.
            else:
                metal = _metal_prices()
                key = _key_prices()
                for i in range(0, len(frame.index)):
                    data = frame.iloc[i]
                    date = data.name
                    if date >= pd.to_datetime('2013-01-01'):
                        currency = data['currency']
                        conversion_rate = _value_at(currency, date, key, metal)
                        frame.iat[i, 0] = 'usd'
                        frame.iat[i, 1] *= conversion_rate[0]
                        frame.iat[i, 2] *= conversion_rate[1]
            self.history = frame

    def to_csv(self, filename):
        """
        Pass-through wrapper that saves the `Item` in CSV.
        :param filename: The filename at which to save the `Item`.
        """
        self.history.to_csv(filename)
    
    def read_csv(self, filename):
        """
        Pass-through wrapper that loads the `Item` in CSV.
        :param filename: The filename from which to load the `Item`.
        """
        self.history = self.history.from_csv(filename)


def _value_at(currency, date, key, metal):
    """
    Converts one currency into USD based on a date. To speed up the operation key and metal are passed to this
    internal method so that the required table lookups only need happen once.
    :param currency: String representing the currency being converted into USD, one of ["usd", "metal", or "keys"].
    :param date: The date of the conversion.
    :param key: A key `DataFrame` history object.
    :param metal: A metal `DataFrame` history object.
    :return: The value of the given currency at the given date in USD.
    """
    f_date = np.datetime64(str(arrow.get(date).format('YYYY-MM-DD')))
    # USD-to-USD conversion is a multiple of 1.
    if currency == "usd":
        return 1, 1
    # Convert metal prices based on historical data.
    elif currency == "metal":
        value_entry = metal.history[:f_date].tail(1)
        return value_entry['value'][0], value_entry['value_high'][0]
    # Convert key prices based on historical data.
    elif currency == "keys":
        value_entry = key.history[:f_date].tail(1)
        metal_conversion = _value_at("metal", date, key, metal)
        return (metal_conversion[0] * value_entry['value'][0],
                metal_conversion[1] * value_entry['value_high'][0])


def _get_key(filename='backpack_tf_account_credentials.json'):
    if filename in [f for f in os.listdir('.') if os.path.isfile(f)]:
        return json.load(open(filename))['credentials']['token']
    else:
        raise IOError(
            'This API requires a backpack.tf credentials token to work. Did you forget to generate one? For more '
            'information refer to:\n\nhttps://backpack.tf/api/pricehistory')


def _metal_prices(filename='metal.csv'):
    """
    Retrieves the metal price table. Since this operation is needed whenever a conversion is made the data is saved
    locally as a CSV and extracted from there.
    :param filename: The filename at which metal prices are saved.
    :return: The `DataFrame` price history object.
    """
    if filename in [f for f in os.listdir('.') if os.path.isfile(f)]:
        ret = Item("")
        ret.read_csv(filename)
        return ret
    else:
        metal = Item("Metal")
        metal.history.loc[pd.to_datetime('2013-01-01')] = ['usd', 0.40, 0.40]
        metal = metal.history.sort_index()
        metal.to_csv('metal.csv')
        return metal


def _key_prices(filename='key.csv'):
    """
    Retrieves the key price table. Since this operation is needed whenever a conversion is made the data is saved
    locally as a CSV and extracted from there.
    :param filename: The filename at which key prices are saved.
    :return: The `DataFrame` price history object.
    """
    if filename in [f for f in os.listdir('.') if os.path.isfile(f)]:
        ret = Item("")
        ret.read_csv(filename)
        return ret
    else:
        key = Item("Mann Co. Supply Crate Key")
        key.to_csv("key.csv")
        return key
