import sys
from mariadb import connect
from mariadb.connections import Connection
from mariadb import Error
import os



def _get_connection() -> Connection:
    try:
        return connect(
            user="admin",
            password=os.environ.get("DB_PASS"),
            host='database-1.ct7kd6mbyts8.eu-west-3.rds.amazonaws.com',
            port=5001,
            database="mydb"
        )
    except Error as e:  # this error Handling doesn't work as expected !
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)


def read_query(sql: str, sql_params=()) -> list:
    with _get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(sql, sql_params)

        return list(cursor)  # what if DELETE statement ?
        # special function needed see delete_query


def delete_query(sql: str, sql_params=()) -> None:
    with _get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(sql, sql_params)
        conn.commit()
    return None


def update_query(sql: str, sql_params=()) -> bool:
    with _get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(sql, sql_params)
        conn.commit()

    return True


def insert_query(sql: str, sql_params=()) -> int:
    with _get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(sql, sql_params)
        conn.commit()

        return cursor.lastrowid


def first_row_query(sql: str, sql_params=()):
    with _get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(sql, sql_params)
        conn.commit()

        # return list(cursor)
        return cursor.fetchone()