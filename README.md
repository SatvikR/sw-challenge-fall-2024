# Cardinal SW Challenge

## File details

Source files are in the root directory of this repo. I've put my data cleaning report in the `docs` directory, and 
I've placed sample output files in the `samples` directory. The following commands were used to generate those files.

```sh
./main.py 3h every_three_hrs.csv
./main.py 1m -s 20240916_00:00:00.00 -e 20240917_00:00:00.00 one_day_every_min.csv
./main.py 1hr30m -s 20240916_00:00:00.00 -e 20240920_00:00:00.00 four_days_every_1hr30.csv
```

# Assumptions and Limitations

### Data Loading

- assumes all the file-names in the data directory are formatted correcrtly, and assumes they are valid CSV's.
- utilizes available cores on the CPU, but does not multithread within each core.
- I did not implement lazy loading, so this does use quite a bit of memory, but (generally) totally fine for a modern computer.

### Data Cleaning

- assumes that the 4 problems are the only 4 problems that exist.
- for the sake of memory, I did not use multiprocessing during cleaning, but (in theory) it would not be difficult to do, if I did away with the in-place cleaning (because of separate virtual memory spaces on separate processes, in-place cleaning would not be possible with multi-processing; I could use threads instead, but it's less scalable and sometimes slower).

### OHLCV Generation

- No major assumptions here, beside that the file path is valid

### CLI Interface

- I did not implement a whole lot of input verification (beyond what is provided by `argparse`), but since I have so few arguments, it should not be a huge hastle to do so.

# Usage Guide

> General Usage

```
./main.py [-h] [-s START_DATE] [-e END_DATE] interval output_file
```

## Positional Arguments

### `interval`

Specifies the interval for each OHLCV sample. Input the interval in the following format:

```
[days]d[hours]h[minutes]m[seconds]s
```

For example, all of the following are valid intervals:

```sh
1d12hrs
30m
1hr45m
30s
```

### `output_file`

Specifies a name of a file to output the generated OHLCV data.

For example,

```
./main.py 30m output.csv
```

## Optional Arguments

### -s, --start_date

Specifices a start date for the generated data, and defaults to the earliest possible timestamp if none is provided. Must be in the following format

```
YYYYMMDD_HH:MM:SS.MS
```

For example, the following is a valid start date which signifies Sept 16th 2024, 9:30 am

```
20240916_09:30:00.00
```

### -e, --end_date

Specifies an end date for the generated data, and defaults to the latests possible timestamp if none if provided. Follows the same format as the start date.

### -h

Prints a help message


