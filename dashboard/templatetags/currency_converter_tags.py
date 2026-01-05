from math import e
from django import template
import decimal
import babel.numbers
from dashboard.models import Currency

#we reister our template tag
register = template.Library()

@register.simple_tag
#converting price with refrence rate select by the user
def price_exchange(curencyCode, value, currentPrice):
    #recuperer la valeur monetaire de base qui est le FCFA
    Fprice = 0
    try:
        baseCurrency = Currency.objects.filter(is_default=True)[0]
        #le priwx en EURO
        if curencyCode == "EUR":
            Fprice = babel.numbers.format_currency(decimal.Decimal(currentPrice) / decimal.Decimal(baseCurrency.exchange_rate), curencyCode)
        else:
            Eurprice = decimal.Decimal(currentPrice) / decimal.Decimal(baseCurrency.exchange_rate)
            #le prix en la monnais choisie
            Fprice = babel.numbers.format_currency(decimal.Decimal(Eurprice) * decimal.Decimal(value), curencyCode)
    except Exception as e:
        print(e)
    return Fprice