import pandas as pd
import numpy as np
import torch
import sqlite3

def merge_and_torchify(hs_df: pd.DataFrame, college_df: pd.DataFrame, years_df: pd.DataFrame, nba_df: pd.DataFrame) -> torch.Tensor:
    
    # Sanitize names - remove commas and periods, and make lowercase
    college_df['Player'].str.replace('.,', "", regex=True).str.lower()
    nba_df['player'].str.replace('.,', "", regex=True).str.lower()
    hs_df['Player'].str.replace('.,', "", regex=True).str.lower()

    # Merge the birthyears column into the college stats df, then convert to age and drop the years column
    college_df = college_df.merge(years_df, how='inner', on='PlayerID')
    college_df['Age'] = college_df['Year']-college_df['BirthYear']
    college_df.drop(columns=['BirthYear'])

    # Send all the dfs to sqlite (other than birthyears because we are done with it)
    con = sqlite3.connect(':memory:')
    college_df.to_sql(name='college', con=con)
    nba_df.to_sql(name='nba', con=con)
    hs_df.to_sql(name='hs', con=con)

    # The goal here is to build a NxMxD tensor where N is the number of players, M is the number of years the player
    # played (padded) and D is the dimension of the stat vector (e.g. points, rebounds, assists, etc.)

    # How do we do identity resolution? This isn't perfect yet, but let's do it by name and year for now.
    college_names = college_df["Player"].unique()
    nba_names = nba_df["player"].unique()
    nba_only_names = np.setdiff1d(nba_names, college_names)
    get_college_pid_query = "SELECT PlayerID, min(Year), max(Year) FROM college WHERE Player=? GROUP BY PlayerID"
    get_nba_pid_query = "SELECT player_id, min(season) FROM nba WHERE player=? GROUP BY player_id"
    cursor = con.cursor()
    # Fill queue with college/NBA player ID pairs
    queue = []
    for player in college_names:
        college_rows = cursor.fetchall(get_college_pid_query, player)
        nba_rows = cursor.fetchall(get_nba_pid_query, player)
        if len(college_rows) > 1 or len(nba_rows) > 1:
            # If we have to match players with the same exact name, figure out the difference between the last year in college and
            # the first year in the league and assign the pairs with the minimum distance
            college_years = np.array(college_rows)[:,2] # max year of college stats
            nba_years = np.array(nba_rows)[:,1] # min year of nba stats
            min_diffs = np.argmin(np.subtract.outer(nba_years, college_years), axis=1)
            for i in range(len(college_rows)):
                queue.append([college_rows[i][0], nba_rows[min_diffs[i]][0]])
        elif len(nba_rows) == 0:
            queue.append([college_rows[0][0], None])
        else:
            queue.append([college_rows[0][0], nba_rows[0][0]])
    for player in nba_only_names:
        nba_rows = cursor.fetchall(get_nba_pid_query, player)
        for i in range(len(nba_rows)):
            queue.append([None, nba_rows[0][0]])

    college_query_base = "SELECT Conference,GP,MPG,PPG,FGM,FGA,FG%,3PM,3PA,3P%,FTM,FTA,FT%,ORB,DRB,RPG,APG,SPG,BPG,TOV,PF,Year,Age FROM college WHERE PlayerID=? ORDER BY Year ASC"
    nba_query_base = "SELECT age,g,mp_per_game,fg_per_game,fga_per_game,fg_percent,x3p_per_game,x3pa_per_game,x3p_percent,ft_per_game,fta_per_game,ft_percent,orb_per_game,drb_per_game,trb_per_game,ast_per_game,stl_per_game,blk_per_game,tov_per_game,pf_per_game,pts_per_game FROM nba WHERE player_id=? ORDER BY season ASC"
    for item in queue:
        if item[0] is not None:
            college_rows = cursor.fetchall(college_query_base, item[0])
        if item[1] is not None:
            nba_rows = cursor.fetchall(nba_query_base, item[1])
