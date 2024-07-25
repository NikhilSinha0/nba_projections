import argparse
import os
import kaggle
import shutil
import subprocess
import sys

def main():
    parser = argparse.ArgumentParser(description='Download all relevant data for NBA projections')
    parser.add_argument('-f', '--force_refresh', help='Deletes existing data and refreshes if flag is set.', action="store_true")
    args = parser.parse_args()

    if not os.path.exists("~/.kaggle/kaggle.json"):
        print("Kaggle credentials not stored. Please follow instructions to get a Kaggle API key (https://www.kaggle.com/docs/api)")
        sys.exit(1)

    # Looks weird but basically get the path for this script, then check if the ../data directory exists relative to this script
    data_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(sys.argv[0]))), "data")

    # Make the directory if it doesn't already exist. If --force is specified, delete the directory and it's contents and recreate it
    if os.path.exists(data_path):
        if not args.force_refresh:    
            print("nba_projections/data already exists, skipping download. If you want to delete the data directory and redownload assets, you can run again with the -f flag.")
            return
        shutil.rmtree(data_path)
    os.makedirs(data_path)

    kaggle.api.dataset_download_file("adityak2003/college-basketball-players-20092021", file_name="CollegeBasketballPlayers2022.csv", path=data_path)
    kaggle.api.dataset_download_file("adityak2003/college-basketball-players-20092021", file_name="CollegeBasketballPlayers2009-2021.csv", path=data_path)
    kaggle.api.dataset_download_file("sumitrodatta/nba-aba-baa-stats", file_name="Player Per Game.csv", path=data_path)
    try:
        subprocess.run(["unzip", os.path.join(data_path, "CollegeBasketballPlayers2022.csv.zip"), "-d", data_path], check=True)
        subprocess.run(["rm", "-rf", os.path.join(data_path, "CollegeBasketballPlayers2022.csv.zip")], check=True)
        subprocess.run(["unzip", os.path.join(data_path, "CollegeBasketballPlayers2009-2021.csv.zip"), "-d", data_path], check=True)
        subprocess.run(["rm", "-rf", os.path.join(data_path, "CollegeBasketballPlayers2009-2021.csv.zip")], check=True)
        subprocess.run(["unzip", os.path.join(data_path, "Player%20Per%20Game.csv.zip"), "-d", data_path], check=True)
        subprocess.run(["rm", "-rf", os.path.join(data_path, "Player%20Per%20Game.csv.zip")], check=True)
        subprocess.run(["mv", os.path.join(data_path, "Player Per Game.csv"), os.path.join(data_path, "Player_Per_Game.csv")], check=True)
    except subprocess.CalledProcessError:
        print("Unzipping the data after downloading was not successful")

if __name__ == '__main__':
    main()
