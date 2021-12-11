# Spotify Data Science Project

## Setup
You will need Git, Python 3.7+, Jupyter Notebook installed on your machine.

To replicate our results, the requirement packages is specified in requiremnets.txt. To install:

(Optional) A virtual machine is highly recommended. Set up guidance:
* With conda:
conda create -n venv python=3.7
conda activate venv
conda install --file requirements.txt

* Without conda:
python3 -m venv venv
souce venv/bin/activate
pip3 install -r requirements.txt

## Usage

### Download datasets
* Download challenger_set.json [here](https://www.aicrowd.com/challenges/spotify-million-playlist-dataset-challenge)
* Download SpotifyFeatures.csv [here](https://www.kaggle.com/zaheenhamidani/ultimate-spotify-tracks-db)


### Collect data from Spotify API
* Collect data for the first dataset
```bash
python extract_data.py challenge_set.json
```
* Collect data for the second dataset
```bash
python get_release_date.py SpotifyFeatures.csv
```
* Run `get_clean_data.ipynb` in Jupyter Notebook to merge 2 datasets

### Analysis
* Run `predict_genre.ipynb` in Jupyter Notebook to see outputs for the models
* Run `predict_popularity.ipynb` in Jupyter Notebook to see outputs for the models
* Run `song_recommender.ipynb` in Jupyter Notebook to see outputs for song recommendation


