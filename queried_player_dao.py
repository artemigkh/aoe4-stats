queried_player_field_names = [
    'profile_id'
]


class QueriedPlayerDao:
    def __init__(self, db_connection):
        self.db_connection = db_connection
        self._profile_insert_statement = QueriedPlayerDao._create_profile_insert_statement()

    def store_queried_player(self, queried_player_id):
        cursor = self.db_connection.cursor()
        cursor.executemany(self._profile_insert_statement, [[queried_player_id]])

        self.db_connection.commit()

    @staticmethod
    def _create_profile_insert_statement():
        return 'INSERT IGNORE INTO queried_player (' + \
               ','.join(queried_player_field_names) + \
               ') VALUES (' + \
               ','.join(['%s'] * len(queried_player_field_names)) + ')'
