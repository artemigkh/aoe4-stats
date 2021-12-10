# Aoe4 Stats
Pulls data from
* `https://aoeiv.net/api/player/matches`
* `https://aoeiv.net/api/player/ratinghistory?game=aoe4`

Combines match entries which have a corresponding rating history entry, and stores it in a SQL
db in tables defined in `database/schema.sql`, which are then used to generate visualizations

## Setup
Any SQL database with `database/schema.sql` applied and connection info supplied in `main.py`
A python3 install with the dependencies in `import` statements `pip3 install` 'd

## Usage
As a courtesy to the volunteers who run `https://aoeiv.net` and their server, the harvester is
set to a rate limit of 10 requests/minute, so would not try more than a couple thousand players.

``` 
python3 ./harvest_data.py
```
to save the api responses to disk

``` 
python3 ./main.py
```
to process the json arrays into the db

The Jupyter notebook `create_visualizations.ipynb` is self-explanatory but requires the first two scripts
to be run first