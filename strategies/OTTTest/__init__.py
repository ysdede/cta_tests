import datetime

from jesse.strategies import Strategy

import custom_indicators as cta


class BBRTest(Strategy):
    def __init__(self):
        super().__init__()
        self.ts = None
        self.output = None
        self.pinescript = f"""//@version=4
study("BBR TEST", precision=2)


tick =
"""

        self.pineplot = """
band1 = hline(1, "Overbought", color=#787B86, linestyle=hline.style_dashed)
band0 = hline(0, "Oversold", color=#787B86, linestyle=hline.style_dashed)
fill(band1, band0, color=color.rgb(38, 166, 154, 90), title="Background")
plot(tick, color=color.lime, style=plot.style_line, linewidth=1)
                """

    def should_long(self) -> bool:
        ratio = cta.bbr(self.candles, 20, 'close', 2.0, True).ratio
        value = round(float(ratio[-1]), 2)

        epoch = self.current_candle[0] / 1000
        self.ts = datetime.datetime.utcfromtimestamp(epoch).strftime('%Y-%m-%d %H:%M')
        year = int(datetime.datetime.utcfromtimestamp(epoch).strftime('%Y'))
        month = int(datetime.datetime.utcfromtimestamp(epoch).strftime('%m'))
        day = int(datetime.datetime.utcfromtimestamp(epoch).strftime('%d'))
        hour = int(datetime.datetime.utcfromtimestamp(epoch).strftime('%H'))

        self.pinescript = self.pinescript + f'\n     year == {year} and month == {month} and dayofmonth == {day} and hour == {hour} ? {value}: '
        self.output = ratio
        return False

    def terminate(self):
        print('Backtest is done')
        print('\n', self.ts, round(self.output[-1], 2))
        self.writepine()

    def writepine(self):
        self.pinescript = self.pinescript + 'na\n'
        self.pinescript = self.pinescript + self.pineplot

        f = open(f"bbr.pine", "w")
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
