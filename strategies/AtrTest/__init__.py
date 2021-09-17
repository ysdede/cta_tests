import datetime

from jesse.strategies import Strategy

import custom_indicators as cta


class AtrTest(Strategy):
    def __init__(self):
        super().__init__()
        self.ts = None
        self.output = None
        self.atr = None
        self.pinescript = f"""//@version=4
study("ATR TEST", precision=2)


tick =
"""

        self.pineplot = """
plot(tick, color=color.red, style=plot.style_line, linewidth=1)
                """

    def should_long(self) -> bool:
        self.atr = cta.atr(self.candles[:, 3], self.candles[:, 4], self.candles[:, 2], length=14, sequential=True)
        value = round(float(self.atr[-1]), 2)

        epoch = self.current_candle[0] / 1000
        self.ts = datetime.datetime.utcfromtimestamp(epoch).strftime('%Y-%m-%d %H:%M')
        year = int(datetime.datetime.utcfromtimestamp(epoch).strftime('%Y'))
        month = int(datetime.datetime.utcfromtimestamp(epoch).strftime('%m'))
        day = int(datetime.datetime.utcfromtimestamp(epoch).strftime('%d'))
        hour = int(datetime.datetime.utcfromtimestamp(epoch).strftime('%H'))

        self.pinescript = self.pinescript + f'\n     year == {year} and month == {month} and dayofmonth == {day} and hour == {hour} ? {value}: '
        self.output = self.atr
        return False

    def terminate(self):
        print('Backtest is done')
        print('\n', self.ts, round(self.output[-1], 2), 'Size: ', self.atr.size)
        self.writepine()

    def writepine(self):
        self.pinescript = self.pinescript + 'na\n'
        self.pinescript = self.pinescript + self.pineplot

        f = open(f"atr.pine", "w")
        f.write(self.pinescript)
        f.close()

    def should_short(self) -> bool:
        return False

    def should_cancel(self) -> bool:
        return True

    def go_long(self):
        pass

    def go_short(self):
        pass
