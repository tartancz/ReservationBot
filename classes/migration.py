class Migration:
    def __init__(self, conn):
        self.conn = conn

    def migrate(self):
        self.conn.executescript('''
            CREATE TABLE "room" (
              "id" integer PRIMARY KEY,
              "name" nvarchar(50) NOT NULL unique,
              "room_size" integer
            );
    
            CREATE TABLE "reservation" (
              "id" integer PRIMARY KEY,
              "room_name" nvarchar(50) NOT NULL,
              reserved bool,
              "day" date DEFAULT CURRENT_TIMESTAMP,
              FOREIGN KEY(room_name) REFERENCES room(name)
            );
            ''')

    def create_rooms(self, data: list[tuple[str, int]]):
        self.conn.executemany('INSERT INTO room(name, room_size) VALUES (?, ?)', data)
        self.conn.commit()