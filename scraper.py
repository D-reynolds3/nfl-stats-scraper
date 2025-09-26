"""
NFL Stats Scraper
-----------------
Scrapes league-wide player season totals (passing, rushing, receiving, defense)
from Pro-Football-Reference and saves them to CSV files.

Usage:
    python scraper.py
"""

import pandas as pd
import os


def scrape_stats(stat_type: str, year: int) -> pd.DataFrame:
    """
    Scrape league-wide season totals for a given stat type and year.

    Parameters:
        stat_type (str): One of "passing", "rushing", "receiving", "defense".
        year (int): Season year to scrape.

    Returns:
        pd.DataFrame: Cleaned DataFrame of stats.
    """
    url = f"https://www.pro-football-reference.com/years/{year}/{stat_type}.htm"
    print(f"Scraping {stat_type} stats for {year} from {url}")

    # Read tables
    tables = pd.read_html(url)
    df = tables[0]

    # Flatten multi-row headers if needed
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.droplevel(0)

    # Remove duplicate header rows
    df = df[df["Player"] != "Player"]

    # Reset index
    df = df.reset_index(drop=True)

    return df


def save_stats(df: pd.DataFrame, stat_type: str, year: int):
    # Create data/year folder if it doesn't exist
    year_folder = os.path.join("data", str(year))
    os.makedirs(year_folder, exist_ok=True)

    # Save inside that folder
    filepath = os.path.join(year_folder, f"{stat_type}.csv")
    df.to_csv(filepath, index=False)
    print(f"Saved {stat_type} stats to {filepath}")



def main():
    year = 2025
    stat_types = ["passing", "rushing", "receiving", "defense"]

    for stat in stat_types:
        df = scrape_stats(stat, year)
        save_stats(df, stat, year)

    print("\n✅ Scraping complete! Data saved in /data folder.")


if __name__ == "__main__":
    main()
