import requests
from pathlib import Path
from bs4 import BeautifulSoup
import os
from pathvalidate import sanitize_filename
from urllib.parse import urljoin, urlparse


def check_for_redirect(response):
    if response.history:
        raise requests.HTTPError


def download_picture(count, soup):
    picture_url = soup.find('div', class_='bookimage').find('a').find('img')['src']
    ext = os.path.splitext(picture_url)[1]
    url = urljoin('https://tululu.org', picture_url)
    response = requests.get(url)
    response.raise_for_status()
    image_folder = 'image'
    Path(image_folder).mkdir(exist_ok=True)
    with open(os.path.join(image_folder, f'{count}{ext}'), 'wb') as file:
        file.write(response.content)


def download_book(count, soup, response):
    title_tag = soup.find('head').find('title')
    title_text = title_tag.text.split('- ')
    name_of_book = f"{sanitize_filename(title_text[0].strip())}.txt"
    book_folder = 'books'
    Path(book_folder).mkdir(exist_ok=True)
    with open(os.path.join(book_folder, f'{count}.{name_of_book}'), 'wb') as file:
        file.write(response.content)


def download_comments(count, soup):
    comments_tag = soup.find_all('div', class_='texts')
    if comments_tag:
        comment_folder = 'comments'
        Path(comment_folder).mkdir(exist_ok=True)
        for comment in comments_tag:
            comment_text = comment.find('span', class_='black')
            with open(os.path.join(comment_folder, f'{count}.txt'), 'a', encoding='utf-8') as file:
                file.write(f'{comment_text.text}\n')


def main():
    for count in range(10):
        book_id = f'{count}'
        payloads = {
            'id': book_id
        }
        book_url = f"https://tululu.org/txt.php"
        try:
            book_response = requests.get(book_url, params=payloads)
            book_response.raise_for_status()
            check_for_redirect(book_response)
            title_page_url = f'https://tululu.org/b{book_id}/'
            title_page_response = requests.get(title_page_url)
            soup = BeautifulSoup(title_page_response.text, 'lxml')
            download_book(count, soup, book_response)
            download_picture(count, soup)
            download_comments(count, soup)
        except requests.HTTPError:
            pass


if __name__ == "__main__":
    main()
