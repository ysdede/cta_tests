import datetime

from jesse.strategies import Strategy, cached

import custom_indicators as cta


class BBTest(Strategy):
    def __init__(self):
        super().__init__()
        self.ts = None
        self.output = None
        self.pinescript = f"""//@version=4
study("BB TEST", precision=2, overlay=true)


tick =
"""

        self.pineplot = """
plot(tick, color=color.lime, style=plot.style_line, linewidth=3)
                """

    # @property
    # @cached
    # def bb(self):
    #     return cta.bb(self.candles, 20, 'close', 2.0, True)

    def should_long(self) -> bool:
        upper = cta.bb(self.candles, 20, 'close', 2.0, True).upper
        value = round(float(upper[-1]), 2)

        epoch = self.current_candle[0] / 1000
        self.ts = datetime.datetime.utcfromtimestamp(epoch).strftime('%Y-%m-%d %H:%M')
        year = int(datetime.datetime.utcfromtimestamp(epoch).strftime('%Y'))
        month = int(datetime.datetime.utcfromtimestamp(epoch).strftime('%m'))
        day = int(datetime.datetime.utcfromtimestamp(epoch).strftime('%d'))
        hour = int(datetime.datetime.utcfromtimestamp(epoch).strftime('%H'))

        self.pinescript = self.pinescript + f'\n     year == {year} and month == {month} and dayofmonth == {day} and hour == {hour} ? {value}: '
        self.output = upper
        return False

    def terminate(self):
        print('Backtest is done')
        print('\n', self.ts, round(self.output[-1], 2))
        self.writepine()

    def writepine(self):
        self.pinescript = self.pinescript + 'na\n'
        self.pinescript = self.pinescript + self.pineplot

        f = open(f"bb.pine", "w")
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
