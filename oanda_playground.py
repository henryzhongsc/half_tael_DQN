import sys
import json

from oandapyV20.contrib.factories import InstrumentsCandlesFactory
from oandapyV20 import API

my_access_token = 'a10a1538b3fdaf3a8a2f3b9a496a3aeb-00a7b8f54791fb3132b22ca77419cc58'
access_token = my_access_token

client = API(access_token=access_token)

_from = "2017-01-01T00:00:00Z"
_to = "2017-06-30T00:00:00Z"
gran = "H4"
instr = "EUR_USD"

params = {
    "granularity": gran,
    "from": _from,
    "to": _to
}

def cnv(r, h):
    for candle in r.get('candles'):
        print(candle)
        ctime = candle.get('time')[0:19]
        try:
            rec = "{time},{complete},{o},{h},{l},{c},{v}".format(
                time=ctime,
                complete=candle['complete'],
                o=candle['mid']['o'],
                h=candle['mid']['h'],
                l=candle['mid']['l'],
                c=candle['mid']['c'],
                v=candle['volume'],
            )
            print(rec)
        except Exception as e:
            print(e, r)
        else:
            h.write(rec+"\n")

with open("/tmp/{}.{}.out".format(instr, gran), "w") as O:
    for r in InstrumentsCandlesFactory(instrument=instr, params=params):
        # print(r)
        print("REQUEST: {} {} {}".format(r, r.__class__.__name__, r.params))
        rv = client.request(r)
        print("RESPONSE:\n{}".format(json.dumps(rv, indent=2)))
        # print("#############################################################################")
        break
        # cnv(r.response, O)