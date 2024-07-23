## NBA Projections

This project aims to project a timeseries of a drafted player's NBA career based on their collegiate stats (or G League Ignite/international league stats), and some other information if it exists like a high school ranking or combine measurements. It will also find the most similar players using vector similarity. Importantly, this projection does not account for players who were drafted with no post-high school experience. This is because high school statistics are hard to come by in a standard format so projecting based off just a ranking is far too volatile. 

### Usage

This project runs through the command line, where you can input the information of a player to project, and then will generate graphs showing a few projection lines. First, we will show the most similar player statistically and their career, as well as a prediction for the input player. The tool will also add a high-end and low-end line to try and predict both the floor and ceiling for the player. This hopefully will give an understanding of what the range of outcomes for the player could be. Each player will generate a graph for minutes, points, rebounds, assists, steals, blocks, and turnovers (all on a per game basis).

### How it works

There are 2 models utilized in this project. The first model projects the length of the player's career. This model is built upon an LSTM with a feedforward network at the end. Once we generate a prediction for the length of the career, we pass the player's data into a second timeseries forecasting model to generate predictions for the player's statistics. We utilize the prediction from the first model as the forecasting window in the second model. This model is utilizing transformers based on the Informer and FEDFormer papers.

### Tools

This project is built mainly using PyTorch for training the models and Matplotlib for displaying the graphs.

### Interesting results

TBD