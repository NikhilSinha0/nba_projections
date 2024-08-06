import os
import sys

def main():
    # Looks weird but basically get the path for this script, then check if the ../data directory exists relative to this script
    data_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(sys.argv[0]))), "data")

    # Make sure the dependent files for running
    if not os.path.exists(data_path) or not os.path.exists(os.path.join(data_path, "hs_rankings.csv")) or not os.path.exists(os.path.join(data_path, "nba_stats.csv")) or not os.path.exists(os.path.join(data_path, "college_stats.csv")):
        print("Couldn't find all dependencies for training. Please run ../util/run before running the training script")
        sys.exit(1)

if __name__ == '__main__':
    main()