import pandas as pd
import torch
import sqlite3

def merge_and_torchify(hs_df: pd.DataFrame, college_df: pd.DataFrame, nba_df: pd.DataFrame) -> torch.Tensor:
    con = sqlite3.connect(':memory:')

    # Sanitize names - remove commas and periods, and make lowercase
    college_df['Player'].str.replace('.,', "", regex=True).str.lower()
    nba_df['player'].str.replace('.,', "", regex=True).str.lower()
    hs_df['Player'].str.replace('.,', "", regex=True).str.lower()

    # Rows are already sorted asc just by nature of how the data was collected for college
    #college_df.groupby("PlayerID", group_keys=True)
    college_df.to_sql(name='college', con=con)

    # For the NBA data, rows are not necessarily ordered so we need to sort and group by ID
    #nba_df.sort_values(by="year", ascending=True).groupby("PlayerID", group_keys=True)
    nba_df.to_sql(name='nba', con=con)

    # Unnecessary to do any grouping for high school since each player should only have one record
    hs_df.to_sql(name='hs', con=con)

    # The goal here is to build a NxMxD tensor where N is the number of players, M is the number of years the player
    # played (padded) and D is the dimension of the stat vector (e.g. points, rebounds, assists, etc.)

    # How do we do identity resolution? This isn't perfect yet, but let's do it by name and year.