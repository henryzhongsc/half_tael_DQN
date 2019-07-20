import oandapyV20
import oandapyV20.endpoints.accounts as accounts
import oandapyV20.endpoints.orders as orders
import oandapyV20.endpoints.pricing as pricing
import oandapyV20.endpoints.positions as positions
import oandapyV20.endpoints.instruments as instruments
from oandapyV20.exceptions import V20Error, StreamTerminated

import time
import datetime
import pandas as pd



class Oanda_Trader:
    def __init__(self, account_ID, access_token):
        self.account_ID = account_ID
        self.access_token = access_token
        self.nationality = "USA"
        self.action = []
        self.trade_history = []

    def clear_history(self):
        self.trade_history=[]
        self.action=[]

    def get_current_price(self, ticker):
        client = oandapyV20.API(access_token=self.access_token)
        params = {
            "instruments": ticker
        }
        rp = pricing.PricingInfo(accountID=self.account_ID, params=params)
        rv = client.request(rp)
        rr = rp.response['prices'][0]
        price = {}
        price['ask'] = float(rr['asks'][0]['price'])
        price['bid'] = float(rr['bids'][0]['price'])
        # print('Current: instrument:  ' + rr.get('instrument')
        #      + ', closeoutAsk:  ' + rr.get('closeoutAsk') + ', closeoutBid:  ' + rr.get('closeoutBid')
        #      + ', time:  ' + rr.get('time'))
        return price

    def create_buy_order(self, ticker, units):
        client = oandapyV20.API(access_token=self.access_token)
        data = {
            "order": {
                "units": 0,
                "instrument": ticker,
                "timeInForce": "FOK",
                "type": "MARKET",
                "positionFill": "DEFAULT"
            }
        }
        data["order"]["units"] = units
        r = orders.OrderCreate(self.account_ID, data=data)
        client.request(r)
        rt = r.response.get('orderFillTransaction')
        rfp = rt.get('fullPrice')

        buy_record = [rt.get('time'), time.mktime(datetime.datetime.strptime(rt.get('time').split('.')[0], "%Y-%m-%dT%H:%M:%S").timetuple()), \
        rt.get('units'), rt.get('instrument'), rt.get('price'), self.get_nav()['marginAvailable'],self.get_nav()['balance'],self.get_nav()['nav'], 'Buy']
        self.trade_history.append(buy_record)
        self.action.append('Buy')
        #print(buy_record)

    def create_sell_order(self, ticker, units):
        client = oandapyV20.API(access_token=self.access_token)
        data = {
            "order": {
                "units": 0,
                "instrument": ticker,
                "timeInForce": "FOK",
                "type": "MARKET",
                "positionFill": "DEFAULT"
            }
        }
        data["order"]["units"] = -units
        r = orders.OrderCreate(self.account_ID, data=data)
        client.request(r)
        rt = r.response.get('orderFillTransaction')
        rfp = rt.get('fullPrice')
        sell_record = [rt.get('time'), time.mktime(datetime.datetime.strptime(rt.get('time').split('.')[0], "%Y-%m-%dT%H:%M:%S").timetuple()), \
        rt.get('units'), rt.get('instrument'), rt.get('price'), self.get_nav()['marginAvailable'],self.get_nav()['balance'],self.get_nav()['nav'], 'Sell']
        self.trade_history.append(sell_record)
        self.action.append('Sell')
        #print(sell_record)

    def close_positions(self, ticker,value = 'ALL'):
        client = oandapyV20.API(access_token=self.access_token)
        positions_ = self.get_positions(ticker)
        if positions_["short"] == 0 and positions_['long'] == 0:
            #print("No position to be closed")
            return -1
            pass
        else:
            if positions_["short"] != 0 and positions_["long"] == 0:
                data = {
                    "shortUnits": value
                }
            elif positions_['short'] == 0 and positions_['long'] != 0:
                data = {"longUnits": value}
            else:
                data = {"shortUnits": value, "longUnits": value}

            r = positions.PositionClose(accountID=self.account_ID, instrument=ticker, data=data)
            client.request(r)

            if positions_["short"] != 0 and positions_["long"] == 0:
                rr = r.response["shortOrderFillTransaction"]
            if positions_["short"] == 0 and positions_["long"] != 0:
                rr = r.response["longOrderFillTransaction"]
            price = rr.get("price")
            unit = rr.get("units")
            instrument = rr.get("instrument")
            t_time = rr.get('time')
            #print(time,datetime.datetime.strptime(time.split('.')[0], "%Y-%m-%dT%H:%M:%S").timetuple())
            unixtime = time.mktime(datetime.datetime.strptime(t_time.split('.')[0], "%Y-%m-%dT%H:%M:%S").timetuple())
            margin = self.get_nav()['marginAvailable']
            accountBalance = self.get_nav()['balance']
            #print(value)
            if value  == 'ALL':
                #print('1')
                close = [t_time, unixtime, unit, instrument, price,margin, accountBalance,self.get_nav()['nav'],'CloseAll']
            else:
                #print('0')
                close = [t_time, unixtime, unit, instrument, price,margin, accountBalance,self.get_nav()['nav'],'Close']
            self.trade_history.append(close)
            #print("")
            return 1

    def stop_profit(self, ticker, percent):
        position = self.get_positions(ticker)
        unit = position["long"] + position["short"]
        if position['unrealizedPL'] >= abs(unit) * percent:
            self.close_positions(ticker)
            self.reset_action()

    def stop_loss(self, ticker, percent):
        position = self.get_positions(ticker)
        print(position)
        unit = position["long"] + position["short"]
        print(position['unrealizedPL'], type(position['unrealizedPL']))
        if position['unrealizedPL'] <= -abs(unit) * percent:
            print(-abs(unit))
            self.close_positions(ticker)
            self.reset_action()
            print("#####!!!!!!#####")

    def get_nav(self):
        account = {}
        client = oandapyV20.API(access_token=self.access_token)
        r = accounts.AccountSummary(self.account_ID)
        client.request(r)
        account['nav'] = float(r.response['account']['NAV'])
        account['balance'] = float(r.response['account']['balance'])
        account['marginAvailable'] = float(r.response['account']['marginAvailable'])
        return account  # return netvalue, and cash balance

    def get_positions(self, ticker):
        position = {}
        client = oandapyV20.API(access_token=self.access_token)
        r = positions.PositionDetails(accountID=self.account_ID, instrument=ticker)
        try:
            rqt = client.request(r)
            position['long'] = float(rqt['position']['long']['units'])
            position['short'] = float(rqt['position']['short']['units'])
            position['unrealizedPL'] = float(rqt['position']['unrealizedPL'])
            position['pl'] = float(rqt['position']['pl'])
        except V20Error:
            position['long'] = 0.0
            position['short'] = 0.0
            position['unrealizedPL'] = 0.0
            position['pl'] = 0.0



        return position  # current open position



    def get_history(self, ticker, time_interval, time_count, to_time, date_time=True):
        client = oandapyV20.API(access_token=self.access_token)
        params = {
            "count": time_count,
            "to": to_time,
            "granularity": time_interval,  # timestep
            "price": "BA"
        }

        r = instruments.InstrumentsCandles(instrument=ticker, params=params)
        client.request(r)
        rr = r.response
        LL = []

        for x in range(0, len(rr['candles'])):
            # if rr['candles'][x]['complete'] == True:
            D = {'highAsk': rr['candles'][x]['ask']['h'], 'highBid': rr['candles'][x]['bid']['h'],
                 'lowAsk': rr['candles'][x]['ask']['l'], 'lowBid': rr['candles'][x]['bid']['l'],
                 'closeAsk': rr['candles'][x]['ask']['c'], 'closeBid': rr['candles'][x]['bid']['c'],
                 'openAsk': rr['candles'][x]['ask']['o'], 'openBid': rr['candles'][x]['bid']['o'],
                 'volume': rr['candles'][x]['volume'], 'time': rr['candles'][x]['time'],
                 'complete': rr['candles'][x]['complete']}
            LL.append(D)

        df = pd.DataFrame(LL).set_index('time')
        if date_time == True:
            df.index = pd.to_datetime(df.index)  # , utc=True)
        # df.index = df.index.tz_convert('US/Eastern')
        df[['highAsk', 'highBid', 'lowAsk', 'lowBid', 'closeAsk', 'closeBid', 'openAsk', 'openBid', 'volume']] = df[
            ['highAsk', 'highBid', 'lowAsk', 'lowBid', 'closeAsk', 'closeBid', 'openAsk', 'openBid', 'volume']].apply(
            pd.to_numeric)
        df["avg"] = (df.closeAsk + df.closeBid) / 2
        # df = df.reset_index(drop=False)
        return df[['highAsk', 'highBid', 'lowAsk', 'lowBid', 'closeAsk', 'closeBid', 'openAsk', 'openBid', 'volume','avg']]

