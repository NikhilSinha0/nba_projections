import pandas as pd
import torch

def merge_and_torchify(hs_df: pd.DataFrame, college_df: pd.DataFrame, nba_df: pd.DataFrame) -> torch.Tensor:
    # Rows are already sorted asc just by nature of how the data was collected for college
    college_df.groupby("PlayerID", group_keys=True)

    # For the NBA data, rows are not necessarily ordered so we need to sort and group by ID
    nba_df.sort_values(by="year", ascending=True).groupby("PlayerID", group_keys=True)
    