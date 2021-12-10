import json
from pathlib import Path

from mysql.connector import connect, Error

from match_record_dao import MatchRecordDao
from queried_player_dao import QueriedPlayerDao


def process_player_json(player_id, mr_dao):
    with open(Path() / 'match-history-json' / player_id, encoding='utf-8') as f:
        original_match_array = json.load(f)

    # Filter to include only match-made 1v1s
    match_array = [m for m in original_match_array if m['num_players'] == 2 and m['name'] == 'AUTOMATCH']

    if len(match_array) == 0:
        print(f"Warning: player with id {match_array} had no valid matches and will be ignored")
        print(f"Original match history was {original_match_array}")
        return

    with open(Path() / 'rating-history-json' / player_id, encoding='utf-8') as f:
        rating_history_array = json.load(f)

    if len(rating_history_array) == 0:
        print(f"Warning: player with id {match_array} had no valid rating history and will be ignored")
        return

    # Augment rating history with whether the update was a win or loss using the previous entry
    rating_history_array = sorted(rating_history_array, key=lambda rh: rh['timestamp'])
    prev_game_total = rating_history_array[0]['num_wins'] + rating_history_array[0]['num_losses']
    for i in range(1, len(rating_history_array)):
        cur_game_total = rating_history_array[i]['num_wins'] + rating_history_array[i]['num_losses']
        if prev_game_total + 1 != cur_game_total:
            # If the entry result can't be determined but has a match, that game will not be included in the stats
            print("Warning: discontinuity in rating history")
            print(prev_game_total)
            print(cur_game_total)
        else:
            rating_history_array[i]['win'] = rating_history_array[i]['num_wins'] > rating_history_array[i - 1][
                'num_wins']
        prev_game_total = cur_game_total

    # Rating history goes back longer, trim the start so they start at same timestamps
    match_timestamps = [match['started'] for match in match_array]
    rating_history_array = [rh for rh in rating_history_array if rh['timestamp'] >= min(match_timestamps)]

    if len(match_array) != len(rating_history_array):
        print(f"Warning: length of match and rating history array differed by "
              f"{abs(len(match_array) - len(rating_history_array))}."
              "Some results will be excluded")

    # Interleave the arrays to match each match result with its rating history update entry
    # (should be directly after each one)
    full_history = sorted(
        [{**{'type': 'MATCH'}, **{'timestamp': match['started']}, **match} for match in match_array] +
        [{**{'type': 'RATING_ENTRY'}, **rh} for rh in rating_history_array],
        key=lambda e: e['timestamp'])

    # Process the interleaved array to match each match with its augmented rating history entry
    i = 0
    while i < len(full_history) - 1:
        if full_history[i]['type'] == 'RATING_ENTRY':
            if i > 0:
                print("Warning: expected MATCH but got 2 RATING_ENTRY in a row. Skipping.")
            i += 1
        elif full_history[i]['type'] == 'MATCH':
            if full_history[i + 1]['type'] == 'RATING_ENTRY':
                print("Successfully matched MATCH to RATING_ENTRY.")

                # If a discontinuity occurred this field will not exist
                if 'win' in full_history[i + 1]:
                    # Update 'won' fields for each player of the match
                    for player_idx in range(2):
                        if full_history[i]['players'][player_idx]['profile_id'] == player_id:
                            full_history[i]['players'][player_idx]['won'] = full_history[i + 1]["win"]
                        else:
                            full_history[i]['players'][player_idx]['won'] = not full_history[i + 1]["win"]
                    mr_dao.store_match_record(full_history[i])

                else:
                    print("Warning: rating entry had no result. Skipping.")

                i += 2
            elif full_history[i + 1]['type'] == 'MATCH':
                i += 1
                print("Warning: expected RATING_ENTRY but got 2 MATCH in a row. Skipping.")


def main():
    con = connect(
        host='localhost',
        user='root',
        password='pass',
        db='aoe4_stats',
        port=3306
    )
    mr_dao = MatchRecordDao(con)
    queried_player_dao = QueriedPlayerDao(con)

    for player_id in (Path() / 'match-history-json').iterdir():
        print(f"Processing player with id {player_id.name}")
        queried_player_dao.store_queried_player(player_id.name)
        process_player_json(player_id.name, mr_dao)


if __name__ == '__main__':
    main()
