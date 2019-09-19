import MySQLdb
from MySQLdb.cursors import DictCursor

from settings import (
    DB_HOST, DB_PORT, DB_USER, DB_PASS,
    DB_NAME
)


class DBHandler:
    connection = None
    cursor = None

    @classmethod
    def connect(cls):
        cls.connection = MySQLdb.connect(
            host=DB_HOST, user=DB_USER,
            password=DB_PASS, db=DB_NAME,
            port=int(DB_PORT),
            use_unicode=True, charset="utf8",
            cursorclass=DictCursor
        )
        cls.cursor = cls.connection.cursor(cursorclass=DictCursor)

    @classmethod
    def _dict_to_sql_str(cls, data) -> str:
        keys = data.keys()
        str_data = ', '.join([f"{x}=%s" for x in keys])

        return str_data

    @classmethod
    def _where_sql_str(cls, where) -> dict:
        str_d = ""
        if not where:
            return {
                'sql': '',
                'values': []
            }
        values = []
        for k in where.keys():
            if isinstance(where[k], list):
                cases = ' '.join([f'{x}' for x in where[k]])
                str_d += f' {k} {cases} '
            else:
                str_d += f' {k} = %s '
                values.append(where[k])

        return {
            'sql': f'WHERE {str_d}',
            'values': values
        }

    @classmethod
    def insert_into_table(cls, table='', data=dict()):
        if not cls.connection:
            cls.connect()

        keys = ', '.join(data.keys())
        values = ', '.join(['%s' for _ in data.keys()])

        query = f"INSERT IGNORE INTO {table} ({keys}) VALUES ({values})"

        d = [x for x in data.values()]

        cls.cursor.execute(query, d)
        cls.connection.commit()
