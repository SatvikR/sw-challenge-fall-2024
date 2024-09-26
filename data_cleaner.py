from statistics import median
from typing import List

from tick_data import Tick

class DataCleaner:

    def __init__(self, rows: List[Tick]):
        self.rows = rows

    def clean_magnitude(self):
        """
        Cleans a list of Tick objects by identifying and correcting anomalous price values.

        This function uses a window-based approach to compare each price value to the median of its surrounding values.
        If a price value is found to be anomalous (i.e., more than 50% different from the median), it is corrected by multiplying it by 10 or 0.1.

        Returns:
            None
        """
        # in order to ensure accuracy, this function is not really efficient, so it should be parallelized.
        window_size = 5 # higher number --> better accuracy
        # if you have lots and lots of anomolous data, window_size should be higher, but 
        # here we assume that for every 5 elements, there will be no more than 2 anomolous elements.

        for i in range(len(self.rows)):
            # create a window around the i'th element, and find any anomlous
            # elements by comparing to the median of the elements in the window
            start = max(0, i - window_size // 2)
            end = min(len(self.rows), i + window_size // 2 + 1)
            # this formulation of start and end ensures that the window is never near empty, 
            # therefore better for accuracy
            # don't include i in the window, because we want to compare it to the median of 
            # surrounding elements, but don't want it to include it in said median.
            window = self.rows[start:i] + self.rows[i+1:end] 
            median_price = median([tick.price for tick in window if tick.price != 0])
            if median_price == 0:
                print(window)
            if abs(self.rows[i].price / median_price - 1) > 0.5: # considers a 50% difference to be an anomaly
                if self.rows[i].price < median_price:
                    self.rows[i].price *= 10.0

    def clean_negative(self):
        """
        Cleans a list of Tick objects by replacing negative prices with their absolute values.

        Returns:
            None
        """
        # super simple; just abs all the prices
        for tick in self.rows:
            tick.price = abs(tick.price)

    def clean_duplicate_timestamps(self):
        """
        Cleans a list of Tick objects by combining duplicate entries based on timestamp.

        Returns:
            None
        """
        # definitely don't parallelize this function, because it potentially removes self.rows from the list
        i = 1
        while i < len(self.rows):
            if self.rows[i].timestamp == self.rows[i-1].timestamp:
                # super simple VWAP (since we only have two elements to average)
                weighted_sum = self.rows[i-1].price * self.rows[i-1].quantity + self.rows[i].price * self.rows[i].quantity
                weighted_avg = weighted_sum / (self.rows[i-1].quantity + self.rows[i].quantity)
                self.rows[i-1].price = weighted_avg
                self.rows[i-1].quantity = self.rows[i-1].quantity + self.rows[i].quantity
                del self.rows[i]
            else:
                i += 1

    def clean_missing_prices(self):
        """
        Cleans a list of Tick objects by replacing missing prices with an interpolation of neighbouring prices.

        Returns:
            None
        """
        def find_non_zero_neighbor(index, direction):
            """
            A helper method to find the nearest non-zero price on either side so we can interpolate between them.
            """
            step = 1 if direction == 'right' else -1
            i = index + step
            while 0 <= i < len(self.rows):
                if self.rows[i].price != 0:
                    return i, self.rows[i].price
                i += step
            return None, None

        for i in range(len(self.rows)):
            if self.rows[i].price == 0:
                left_index, left_value = find_non_zero_neighbor(i, 'left')
                right_index, right_value = find_non_zero_neighbor(i, 'right')
                if left_index is None and right_index is None:
                    # All prices are zero, can't interpolate
                    continue
                elif left_index is None: # no non-zero neighbours on the left
                    self.rows[i].price = right_value
                elif right_index is None: # no non-zero neighbours on the right
                    self.rows[i].price = left_value
                else:
                    # interpolate
                    self.rows[i].price = (left_value + right_value) / 2.0

    
    def clean(self) -> List[Tick]:
        """
        Cleans the time-series data by removing anomalies and inconsistencies. 
        """
        self.clean_negative()
        self.clean_magnitude()
        self.clean_missing_prices()
        self.clean_duplicate_timestamps()

