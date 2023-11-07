import requests
from pathlib import Path
from bs4 import BeautifulSoup
import os
from pathvalidate import sanitize_filename
from urllib.parse import urljoin
import argparse
import time


def check_for_redirect(response):
    if response.history:
        raise requests.HTTPError


def download_picture(count, book_cover_url):
    ext = os.path.splitext(book_cover_url)[1]
    url = urljoin(f'https://tululu.org/b{count}/', book_cover_url)
    response = requests.get(url)
    response.raise_for_status()
    image_folder = 'image'
    Path(image_folder).mkdir(exist_ok=True)
    with open(os.path.join(image_folder, f'{count}{ext}'), 'wb') as file:
        file.write(response.content)


def download_book(count, book_title):
    payloads = {
            'id': count
        }
    book_url = f"https://tululu.org/txt.php"
    book_response = requests.get(book_url, params=payloads)
    book_response.raise_for_status()
    check_for_redirect(book_response)
    book_name = f"{book_title}.txt"
    book_folder = 'books'
    Path(book_folder).mkdir(exist_ok=True)
    with open(os.path.join(book_folder, f'{count}.{book_name}'), 'wb') as file:
        file.write(book_response.content)


def download_comments(count, comments):
    comment_folder = 'comments'
    Path(comment_folder).mkdir(exist_ok=True)
    with open(os.path.join(comment_folder, f'{count}.txt'), 'a', encoding='utf-8') as file:
        for comment in comments:
            file.write(f'{comment}\n')


def parse_book_page(response):
    soup = BeautifulSoup(response.text, 'lxml')
    title_tag = soup.find('head').find('title')
    title_text = title_tag.text.split(' - ')
    genre_tag = soup.find('span', class_='d_book').find('a')
    genre = genre_tag['title'].split(' - ')[0]
    picture_url = soup.find('div', class_='bookimage').find('a').find('img')['src']
    comments_tag = soup.find_all('div', class_='texts')
    comments = [comment.find('span', class_='black').text for comment in comments_tag]
    return {'book_title': sanitize_filename(title_text[0]),
            'book_author': title_text[1].split(',')[0],
            'book_genre': genre,
            'book_cover_url': picture_url,
            'comments_on_book': comments}


def main():
    parser = argparse.ArgumentParser(description='''Программа позволяет скачать книги, их обложки и комментарии с сайта https://tululu.org/.
                                     Для начала работы желательно выбрать с какого(start_id) по какой(end_id) ID скачивать книги''')
    parser.add_argument('--start_id', type=int, default=10, help='ID первой книги')
    parser.add_argument('--end_id', type=int, default=25, help='ID второй книги')
    args = parser.parse_args()
    start_id = args.start_id
    end_id = args.end_id
    for count in range(start_id, end_id):
        try:
            url = f'https://tululu.org/b{count}/'
            response = requests.get(url)
            response.raise_for_status()
            check_for_redirect(response)
            book = parse_book_page(response)
            download_book(count, book['book_title'])
            download_picture(count, book['book_cover_url'])
            if book['comments_on_book']:
                download_comments(count, book['comments_on_book'])
        except requests.HTTPError:
            print('HTTP error occurred')
        except requests.ConnectionError:
            print('Connection is interrupted')
            time.sleep(300)


if __name__ == "__main__":
    main()
