import csv
from dataclasses import dataclass
import os
from multiprocessing import Pool
from datetime import datetime
from typing import List, Self
from tick_data import Tick


def load_file(path: str) -> List[Tick]:
    """
    Read an individual csv file -- will be used in a thread pool, below.
    """
    rows = []
    with open(path) as f:
        reader = csv.reader(f)
        next(reader)  # skip the first line, which is the header
        for row in reader:
            rows.append(Tick(
                timestamp=datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S.%f"),
                price=float(row[1]) if row[1] else 0.0,
                quantity=int(row[2])
            ))
    return rows


@dataclass
class TickFileMetadata:
    """
    Represents the metadata gathered from the name of a tick file
    """
    file_path: str
    ticker: str
    day: datetime
    series: int
    hash: str

    def read_metadata(directory: str, file_name: str) -> Self:
        """
        Reads metadata from a file name and returns a TickFileMetadata object.

        Args:
            file_name (str): The name of the file to read metadata from.

        Returns:
            TickFileMetadata: A TickFileMetadata object containing the file name, ticker, day, series, and hash.
        """
        raw_metadata = file_name.replace('.csv', '').split('_')
        return TickFileMetadata(
            file_path=os.path.join(directory, file_name),
            ticker=raw_metadata[0],
            day=datetime.strptime(
                raw_metadata[2], '%Y%m%d'),  # year, month, day
            series=int(raw_metadata[3]),
            hash=raw_metadata[4]
        )


class DataLoader():
    """
    Loads time-series data from csv files in a directory.
    """

    def __init__(self, path: str):
        """
        Initializes a DataLoader object.

        Args:
            path (str): The path to the data directory, assumes all file names in the directory are formatted correctly.

        Returns:
            None
        """
        self.files = [TickFileMetadata.read_metadata(
            path, f) for f in sorted(os.listdir(path))]
        self.rows = []

    def load(self, start_date: datetime = datetime.min, end_date: datetime = datetime.max) -> List[Tick]:
        """
        Loads time-series data from csv files in a directory within a specified date range.

        Args:
            start_date (datetime): The start date of the range (inclusive). Defaults to datetime.min.
            end_date (datetime): The end date of the range (inclusive). Defaults to datetime.max.

        Returns:
            List[Tick]: a list of all the tick data
        """
        # filter out files that are not in our date range
        file_list = [
            f.file_path for f in self.files if start_date <= f.day <= end_date]

        # using a process pool here instead of a thread pool beacause we have thousands of files to process,
        # and this is generally more scalable.
        # default behavior of Pool is to use the same number of cores as is available on the CPU.
        with Pool() as pool:
            frames = pool.map(load_file, file_list)

        # join all the frames into one big frame (self.rows)
        for frame in frames:
            self.rows.extend(frame)

        return self.rows
