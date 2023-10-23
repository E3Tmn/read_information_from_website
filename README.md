# Скачиваем книги с сайта
Программа позволяет скачать книги, их обложки и комментарии с сайта https://tululu.org/
## Зависимости
Python должен быть уже установлен. Для установки необходимым библиотек используйте файл `requirements.text`.
```bash
pip install -r requirements.txt
```
## Запуск
Запуск на Windows.
```bash
python main.py
```
Для того, чтобы скачать книги по нужным Вам ID используйте `start_id` - id первой книги, `end_id` - id второй книги.
```bash
python main.py --start_id 10 --end_id 25
```
