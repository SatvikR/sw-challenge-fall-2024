import csv
from typing import List

from tick_data import Tick


class OHLCVGen:
    """
    Generates the output OHLCV data. Designed so that one generator object can generate multiple OHLCV's for a given data range.
    """
    def __init__(self, rows: List[Tick]):
        self.rows = rows

    def generate(self, interval, start_date, end_date, output_file):
        """
        Generates an output csv file. Ensures that all intervals are between start_date and end_date. Expects cleaned data.
        """
        with open(output_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['timestamp', 'open', 'high',
                            'low', 'close', 'volume'])

            # Some clamping is necessary here because, for efficiency, data loading over-loads some data
            interval_start = max(start_date, self.rows[0].timestamp)
            interval_end = interval_start + interval
            end_date = min(end_date, self.rows[-1].timestamp)

            i = 0
            while interval_end < end_date:
                # Track the OLHCV data points for this interval
                interval_open = 0
                interval_max = float('-inf')
                interval_low = float('inf')
                interval_volume = 0

                # add as many data points as possible to this interval.
                while i < len(self.rows) and interval_start <= self.rows[i].timestamp < interval_end:
                    if not interval_open:
                        interval_open = self.rows[i].price

                    interval_volume += self.rows[i].quantity
                    interval_max = max(interval_max, self.rows[i].price)
                    interval_low = min(interval_low, self.rows[i].price)
                    i += 1

                # only add this to the spreadsheet if there was any actual trading activity during the interval
                if interval_open:
                    writer.writerow([str(interval_start), interval_open, interval_max,
                                    interval_low, self.rows[i-1].price, interval_volume])

                # move to next interval
                interval_start = interval_end
                interval_end = interval_start + interval
