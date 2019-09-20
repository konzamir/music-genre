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

    @classmethod
    def update_table_data(cls, table='', data=dict(), where=dict()):
        if not cls.connection:
            cls.connect()

        data_sql = ''
        if data:
            str_d = cls._dict_to_sql_str(data)
            data_sql = f'SET {str_d}'

        where_sql = cls._where_sql_str(where)

        sql = f"UPDATE {table} {data_sql} {where_sql['sql']}"

        d = [x for x in data.values()]
        d.extend(where_sql['values'])

        cls.cursor.execute(sql, d)
        cls.connection.commit()

    @classmethod
    def get_data_from_table(cls, table='', limit=0, offset=0, table_fields=[], join_table_fields=[],
                            where=dict(), join_table=None, join_relation={}):
        if not cls.connection:
            cls.connect()

        where_sql = cls._where_sql_str(where)

        inner_join_sql = ''
        if join_table:
            inner_join_sql = f"INNER JOIN {join_table} ON {table} " + \
                             f".{join_relation['main_table_field']} = " + \
                             f"{join_table}.{join_relation['join_table_field']}"

        limit_sql = ''
        if limit:
            limit_sql = f"LIMIT {limit}"

        offset_sql = ''
        if offset:
            offset_sql += f"OFFSET {offset}"

        select_columns = '*'
        if table_fields and join_table_fields:
            select_columns = ', '.join([f'{table}.{x}' for x in table_fields])
            select_columns += ', ' + ', '.join([f'{join_table}.{x}' for x in join_table_fields])

        sql = f"SELECT {select_columns} from {table} {inner_join_sql} {where_sql['sql']} {limit_sql} {offset_sql}"

        d = []
        d.extend(where_sql['values'])

        cls.cursor.execute(sql, d)
        result = cls.cursor.fetchall()
        return result

    @classmethod
    def delete_from_table(cls, table='', where=dict()):
        if not cls.connection:
            cls.connect()

        where_sql = cls._where_sql_str(where)
        sql = f"DELETE FROM {table} {where_sql['sql']}"
        d = where_sql['values']
        cls.cursor.execute(sql, d)
        cls.connection.commit()
