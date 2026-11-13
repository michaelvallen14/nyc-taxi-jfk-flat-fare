"""
Download all raw datasets required for MAST30034 Project 1.

Fetches NYC TLC Yellow Taxi and High Volume FHV trip records for
January-June 2025, the taxi zone lookup table and shapefile, and
BTS Airline On-Time Performance data for the same window.

Usage:
    python scripts/download_data.py
"""

from pathlib import Path
from urllib.request import urlretrieve

TLC_BASE = "https://d37ci6vzurychx.cloudfront.net"
BTS_BASE = "https://transtats.bts.gov/PREZIP"
YEAR = 2025
MONTHS = range(1, 7)

LANDING = Path(__file__).parent.parent / "data" / "landing"


def download_trip_data(dataset: str, prefix: str, out_dir: Path) -> None:
    """
    Download monthly TLC trip record parquet files.

    Args:
        dataset: TLC filename stem, e.g. 'yellow_tripdata'.
        prefix: Local filename prefix, e.g. 'yellow'.
        out_dir: Directory to write the parquet files into.
    """
    out_dir.mkdir(parents=True, exist_ok=True)

    for month in MONTHS:
        mm = f"{month:02d}"
        url = f"{TLC_BASE}/trip-data/{dataset}_{YEAR}-{mm}.parquet"
        dest = out_dir / f"{prefix}_{YEAR}-{mm}.parquet"

        if dest.exists():
            print(f"Skipping {dest.name}, already present")
            continue

        print(f"Downloading {dest.name}")
        urlretrieve(url, dest)


def download_zone_data(out_dir: Path) -> None:
    """Download the taxi zone lookup table and shapefile."""
    out_dir.mkdir(parents=True, exist_ok=True)

    for filename in ("taxi_zone_lookup.csv", "taxi_zones.zip"):
        dest = out_dir / filename
        if dest.exists():
            print(f"Skipping {filename}, already present")
            continue
        print(f"Downloading {filename}")
        urlretrieve(f"{TLC_BASE}/misc/{filename}", dest)


def download_bts_data(out_dir: Path) -> None:
    """
    Download BTS Reporting Carrier On-Time Performance monthly zips.

    Each zip contains one CSV of all US domestic flights for that month, plus
    a readme.html. Filter to Dest == "JFK" for JFK arrivals. Not unzipped here
    to match the raw/immutable convention of the landing zone.
    """
    out_dir.mkdir(parents=True, exist_ok=True)

    for month in MONTHS:
        filename = (
            f"On_Time_Reporting_Carrier_On_Time_Performance_1987_present_{YEAR}_{month}.zip"
        )
        dest = out_dir / filename

        if dest.exists():
            print(f"Skipping {filename}, already present")
            continue

        print(f"Downloading {filename}")
        urlretrieve(f"{BTS_BASE}/{filename}", dest)


if __name__ == "__main__":
    download_trip_data("yellow_tripdata", "yellow", LANDING / "yellow")
    download_trip_data("fhvhv_tripdata", "fhvhv_tripdata", LANDING / "hvfhv")
    download_zone_data(LANDING / "misc")
    download_bts_data(LANDING / "bts")
    print("Done")