#!/bin/sh

set -x

rm -r samples
mkdir samples

./main.py 3h ./samples/every_three_hrs.csv
./main.py 1m -s 20240916_00:00:00.00 -e 20240917_00:00:00.00 ./samples/one_day_every_min.csv
./main.py 1hr30m -s 20240916_00:00:00.00 -e 20240920_00:00:00.00 ./samples/four_days_every_1hr30.csv
