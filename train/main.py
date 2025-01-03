import os
import sys
import pandas as pd
import torch
from torch.utils.data import DataLoader
from matplotlib import pyplot as plt

def main():
    # Looks weird but basically get the path for this script, then check if the ../data directory exists relative to this script
    data_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(sys.argv[0]))), "data")

    dep_files = ["hs_rankings.csv", "nba_stats.csv", "college_stats.csv", "college_birthyears.csv"]
    # Make sure the dependent files for running
    if not os.path.exists(data_path):
        print("Couldn't find dependencies folder for training. Please run ../util/run before running the training script")
        sys.exit(1)
    for file in dep_files:
        if not os.path.exists(os.path.join(data_path, file)):
            print(f"Couldn't find all dependencies for training. Missing {file}. Please run ../util/run before running the training script")
            sys.exit(1)

if __name__ == '__main__':
    main()