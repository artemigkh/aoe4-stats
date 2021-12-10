match_record_field_names = [
    'match_id',
    'lobby_id',
    'start_time',
    'server',
    'game_version',
    'map_type',
    'player1_profile_id',
    'player1_civ',
    'player1_win',
    'player2_profile_id',
    'player2_civ',
    'player2_win',
    'winning_civ',
    'losing_civ'
]


class MatchRecordDao:
    def __init__(self, db_connection):
        self.db_connection = db_connection
        self._match_record_insert_statement = MatchRecordDao._create_match_record_insert_statement()

    def store_match_record(self, match_record):
        cursor = self.db_connection.cursor()
        cursor.executemany(self._match_record_insert_statement, [[
            match_record['match_id'],
            match_record['lobby_id'] if 'lobby_id' in match_record else '',
            match_record['timestamp'],
            match_record['server'],
            match_record['version'],
            match_record['map_type'],
            match_record['players'][0]['profile_id'],
            match_record['players'][0]['civ'],
            match_record['players'][0]['won'],
            match_record['players'][1]['profile_id'],
            match_record['players'][1]['civ'],
            match_record['players'][1]['won'],
            match_record['players'][0]['civ'] if match_record['players'][0]['won'] else match_record['players'][1]['civ'],
            match_record['players'][1]['civ'] if match_record['players'][1]['won'] else match_record['players'][0]['civ']
        ]])

        self.db_connection.commit()

    @staticmethod
    def _create_match_record_insert_statement():
        return 'INSERT IGNORE INTO match_record (' + \
               ','.join(match_record_field_names) + \
               ') VALUES (' + \
               ','.join(['%s'] * len(match_record_field_names)) + ')'
