import requests
import json

keys = {
    'рубль': 'RUB',
    'доллар': 'USD',
    'евро': 'EUR'
}

class APIException(Exception):
    pass

class CurrencyConverter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        if quote == base:
            raise APIException('Введите разные валюты')
        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'Нет такой валюты "{quote}"')
        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'Нет такой валюты "{base}"')
        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Неизвестное число "{amount}"')
        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = json.loads(r.content)[keys[base]]*amount
        return total_base