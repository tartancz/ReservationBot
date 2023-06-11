import sqlite3
from pathlib import Path
from .scraper import Scraper


class Database:
    def __init__(self, fp: Path, scraper: Scraper):
        self.fp = fp
        conn = sqlite3.connect(fp)
        # if db is not valid, make migrations
        if not self.valid_db(conn):
            from .migration import Migration
            mig = Migration(conn)
            mig.migrate()
            # create tables
            mig.create_rooms(scraper.get_rooms())
        conn.close()

    def valid_db(self, conn) -> bool:
        """
        check if db have valid tables for program
        :param conn: connection to db
        :return: true = valid, false = invalid
        """
        res = conn.execute("SELECT name FROM sqlite_master")
        tables = [row[0] for row in res]
        is_valid = 'room' in tables and 'reservation' in tables
        return is_valid

    def save_reservation(self, reservation: dict[str, bool]):
        data = []
        for key, value in reservation.items():
            row_data = (key, value)
            data.append(row_data)
        conn = sqlite3.connect(self.fp)
        conn.executemany("INSERT INTO RESERVATION(room_name, reserved) VALUES(?, ?)", data)
        conn.commit()
        conn.close()
