import requests
from pathlib import Path


def main():
    for count in range(10):
        url = f"https://tululu.org/txt.php?id=3216{count}"
        response = requests.get(url)
        response.raise_for_status()
        Path('books').mkdir(exist_ok=True)
        filename = f'text{count}.txt'
        with open(f'books/{filename}', 'wb') as file:
            file.write(response.content)


if __name__ == "__main__":
    main()
