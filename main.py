import time

from classes import scraper, database
from pathlib import Path
import schedule


def main():
    scr = scraper.Scraper("") #insert url of website

    db = database.Database(
        Path("./database.db"),
        scr
    )

    def save():
        db.save_reservation(scr.parse())

    schedule.every().day.at('22:00').do(save)

    while True:
        schedule.run_pending()
        time.sleep(3600)


if __name__ == "__main__":
    main()
