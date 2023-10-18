import requests
from pathlib import Path


def check_for_redirect(response):
    if response.history:
        raise requests.HTTPError


def main():
    for count in range(10):
        payloads = {
            'id': f'3216{count}'
        }
        url = f"https://tululu.org/txt.php"
        try:
            response = requests.get(url,params=payloads)
            response.raise_for_status()
            check_for_redirect(response)
            Path('books').mkdir(exist_ok=True)
            filename = f'text{count}.txt'
            with open(f'books/{filename}', 'wb') as file:
                file.write(response.content)
        except requests.HTTPError:
            print(requests.HTTPError)


if __name__ == "__main__":
    main()
