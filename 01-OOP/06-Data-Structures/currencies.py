# pylint: disable=missing-docstring
# pylint: disable=fixme
# pylint: disable=unused-argument

from logging import captureWarnings


RATES = {"USDEUR":0.85,"GBPEUR":1.13,"CHFEUR":0.86} # TODO: add some currency rates

# `amount` is a `tuple` like (100, EUR). `currency` is a `string`
def convert(amount, currency):
    val,currency_dep=amount
    clef=currency_dep+currency
    if currency_dep not in "".join(RATES):
        return None
    rate=RATES[clef]
    return round(val*rate,0)
    pass # TODO
