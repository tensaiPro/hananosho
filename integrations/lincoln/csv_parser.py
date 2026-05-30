import csv
import glob
import os


DOWNLOAD_DIR = r"C:\download"


def get_latest_csv():

    files = glob.glob(
        os.path.join(
            DOWNLOAD_DIR,
            "*.csv"
        )
    )

    if not files:
        raise FileNotFoundError(
            "CSVが見つかりません"
        )

    return max(
        files,
        key=os.path.getmtime
    )


def parse_reservation_csv():

    csv_file = get_latest_csv()

    rows = []

    with open(
        csv_file,
        encoding="cp932",
        newline=""
    ) as f:

        reader = csv.DictReader(f)

        for row in reader:

            rows.append(row)

    return rows
