#!/usr/bin/env python3
import re
from data_cleaner import DataCleaner
from data_loader import DataLoader
from datetime import datetime, timedelta
import time
import argparse

from ohlcv_gen import OHLCVGen

def parse_time_interval(s: str):
    """
    Parses a time interval string into its constituent parts.

    Args:
        s (str): The time interval string to parse.

    Returns:
        A list of tuples containing the time interval value and unit.
    """
    # regex for each of the units, separately, so that we can add them after
    pattern = r'(\d+)([smhd])'
    matches = re.findall(pattern, s)

    # map over our units to the datetime timedelta arguments
    unit_map = {
        's': 'seconds',
        'm': 'minutes',
        'h': 'hours',
        'd': 'days'
    }

    # gather all the timedelta arguments into a dictionary
    delta_args = {}
    for val, unit in matches:
        delta_args[unit_map[unit]] = int(val)

    # spread the dictionary to the timedelta constructor
    return timedelta(**delta_args)


def parse_date(s: str):
    return datetime.strptime(s, "%Y%m%d_%H:%M:%S.%f")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="An interface to work with CTG tick data.")
    parser.add_argument("interval", help="the time interval between output OHLCV data.", type=str)
    parser.add_argument("output_file", help="path to the output file to create.", type=str)
    parser.add_argument("-s", "--start_date", help="the start date of the data to output. defaults to the minimum datetime in python. Expects YYYYMMDD_HH:MM:SS.MS", type=str)
    parser.add_argument("-e", "--end_date", help="the end date of the data to output. defaults to the maximum datetime in python. Expects YYYYMMDD_HH:MM:SS.MS", type=str)
    args = parser.parse_args()

    out_file = args.output_file
    interval = parse_time_interval(args.interval)
    start_date = parse_date(args.start_date) if args.start_date else datetime.min
    end_date = parse_date(args.end_date) if args.end_date else datetime.max

    start_time = time.time()
    d = DataLoader('./data')
    data = d.load(start_date, end_date)
    end_time = time.time()

    print(f"{end_time - start_time} seconds to load data")

    start_time = time.time()
    cleaner = DataCleaner(data)
    cleaner.clean()
    end_time = time.time()

    print(f"{end_time - start_time} seconds to clean data")

    start_time = time.time()
    gen = OHLCVGen(data)
    gen.generate(interval, start_date, end_date, out_file)
    end_time = time.time()

    print(f"{end_time - start_time} seconds to generate output")