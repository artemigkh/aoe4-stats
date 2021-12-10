import json
from pathlib import Path

import requests
import time


def save_response(url, save_loc):
    print(f"GET {url}")
    r = requests.get(url)
    print(f"Status: {r.status_code}")

    if r.status_code == 200:
        with open(str(save_loc), 'w') as out:
            json.dump(r.json(), out)
            print(f"Saved to {save_loc}")
    else:
        print(r.__dict__)
    time.sleep(6)


def main():
    match_history_json_folder = Path() / 'match-history-json'
    rating_history_json_folder = Path() / 'rating-history-json'
    match_history_json_folder.mkdir(exist_ok=True)
    rating_history_json_folder.mkdir(exist_ok=True)

    leaderboard_json = requests.get("https://aoeiv.net/api/leaderboard?game=aoe4&leaderboard_id=17&start=1&count=1000")
    total = len(leaderboard_json.json()['leaderboard'])
    for cur, entry in enumerate(leaderboard_json.json()['leaderboard']):
        print(f"Processing entry {cur}/{total}")
        profile_id = str(entry['profile_id'])

        save_response(
            f"https://aoeiv.net/api/player/matches?game=aoe4&profile_id={profile_id}&count=500",
            match_history_json_folder / profile_id
        )
        save_response(
            f"https://aoeiv.net/api/player/ratinghistory?game=aoe4&leaderboard_id=17&profile_id={profile_id}&count=500",
            rating_history_json_folder / profile_id
        )


if __name__ == '__main__':
    main()
