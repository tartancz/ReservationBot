from bs4 import BeautifulSoup
import requests

# headers to look like browser
HEADERS = {
    'authority': 'www.penzion-na-sedmicce.cz',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'cs-CZ,cs;q=0.9',
    'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
}


class Scraper:
    def __init__(self, url, parser='html.parser'):
        self.url = url
        self.parser = parser

    def parse(self) -> dict[str, bool]:
        html = self.get_html()
        a = self.get_reservation_information(html)
        print(self.get_reservation_information(html))
        return a

    def get_rooms(self):
        rooms_names = []
        html = self.get_html()
        soup = BeautifulSoup(html, 'html.parser')
        for room in soup.find_all('div', class_="room-item-image-frame"):
            room_name = room.find_next("h3").text
            elems = room.find_all_next('span', class_="icon-text", limit=2)
            # get text of elemets
            room_size, _ = [elem.text for elem in elems]
            rooms_names.append((room_name, room_size))
        return rooms_names

    def get_html(self) -> str:
        response = requests.get(self.url, headers=HEADERS)
        return response.text

    def get_reservation_information(self, html: str) -> dict[str, bool]:
        result = {}
        soup = BeautifulSoup(html, 'html.parser')
        # find all rooms from html
        for room in soup.find_all('div', class_="room-item-image-frame"):
            room_name = room.find_next("h3").text
            # get list of 2 span elements where firs one is room_size
            # and second if its reserved
            elems = room.find_all_next('span', class_="icon-text", limit=2)
            # get text of elemets
            _, reserved_text = [elem.text for elem in elems]
            # element of span return "volno" or date
            result[room_name] = reserved_text != "Volno"
        return result
