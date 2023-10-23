import requests
from pathlib import Path
from bs4 import BeautifulSoup
import os
from pathvalidate import sanitize_filename
from urllib.parse import urljoin, urlparse


def download_picture(count, soup):
    picture_url = soup.find('div', class_='bookimage').find('a').find('img')['src']
    print(os.path.splitext(picture_url))
    url = urljoin('https://tululu.org', picture_url)
    path = urlparse(url).path
    ext = os.path.splitext(path)[1]
    response = requests.get(url)
    response.raise_for_status()
    image_folder = 'image'
    Path(image_folder).mkdir(exist_ok=True)
    with open(os.path.join(image_folder, f'{count}{ext}'), 'wb') as file:
        file.write(response.content)


def check_for_redirect(response):
    if response.history:
        raise requests.HTTPError


def get_title_of_book(soup):
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
        book_url = f"https://tululu.org/txt.php"
        try:
            response = requests.get(book_url, params=payloads)
            response.raise_for_status()
            check_for_redirect(response)
            title_page_url = f'https://tululu.org/b{book_id}/'
            title_page_response = requests.get(title_page_url)
            soup = BeautifulSoup(title_page_response.text, 'lxml')
            filename = get_title_of_book(soup)
            download_picture(count, soup)
            book_folder = 'books'
            Path(book_folder).mkdir(exist_ok=True)
            with open(os.path.join(book_folder, f'{count}.{filename}'), 'wb') as file:
                file.write(response.content)
        except requests.HTTPError:
            pass


if __name__ == "__main__":
    main()
