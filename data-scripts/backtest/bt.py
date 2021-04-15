from bitmex_backtest import Backtest

bt = Backtest(test=True)
filepath = "xbtusd_4H.csv"
if bt.exists(filepath):
    bt.read_csv(filepath)
else:
    params = {
        "resolution": "60",  # 1 hour candlesticks (default=1) 1,3,5,15,30,60,120,180,240,360,720,1D,3D,1W,2W,1M
        "count": "21192" # 5000 candlesticks (default=500)
    }
    bt.candles("XBTUSD", params)
    bt.to_csv(filepath)

fast_ma = bt.ema(period=12)
slow_ma = bt.ema(period=26)
# exit_ma = bt.sma(period=5)
bt.buy_entry = (fast_ma > slow_ma) & (fast_ma.shift() <= slow_ma.shift())
bt.sell_entry = (fast_ma < slow_ma) & (fast_ma.shift() >= slow_ma.shift())

bt.buy_exit = (bt.C < slow_ma) & (bt.C.shift() >= slow_ma.shift())
bt.sell_exit = (bt.C > slow_ma) & (bt.C.shift() <= slow_ma.shift())

bt.quantity = 100 # default=1
# bt.stop_loss = 200 # stop loss (default=0)
# bt.take_profit = 1000 # take profit (default=0)

print(bt.run())
bt.plot("backtest.png")