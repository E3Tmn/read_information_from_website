import requests
from pathlib import Path
from bs4 import BeautifulSoup
import os
from pathvalidate import sanitize_filename


def check_for_redirect(response):
    if response.history:
        raise requests.HTTPError


def get_title_of_book(book_id):
    url = f'https://tululu.org/b{book_id}/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    title_tag = soup.find('head').find('title')
    title_text = title_tag.text.split('- ')
    name_of_book = title_text[0].strip()
    return f"{sanitize_filename(name_of_book)}.txt"


def main():
    for count in range(10):
        book_id = f'3216{count}'
        payloads = {
            'id': book_id
        }
        url = f"https://tululu.org/txt.php"
        try:
            response = requests.get(url,params=payloads)
            response.raise_for_status()
            check_for_redirect(response)
            filename = get_title_of_book(book_id)
            folder='books'
            Path(folder).mkdir(exist_ok=True)
            with open(os.path.join(folder,f'{count}.{filename}'), 'wb') as file:
                file.write(response.content)
        except requests.HTTPError:
            print(requests.HTTPError)


if __name__ == "__main__":
    main()
