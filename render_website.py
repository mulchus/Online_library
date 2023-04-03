import json
import argparse
import sys

from urllib import parse
from more_itertools import chunked
from jinja2 import Environment, FileSystemLoader, select_autoescape
from pathlib import Path
from livereload import Server


PAGES_DIRECTORY = 'pages'
BOOK_CARDS_PER_PAGE = 40


def on_reload():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    parser = argparse.ArgumentParser(description='Сайт для чтения книг, скачанных с https://tululu.org/.')
    parser.add_argument(
        '--json_path',
        nargs='?',
        type=Path,
        default='media/about_books.json',
        help='путь и имя файла о книгах .json'
    )
    parser_args = parser.parse_args()
    try:
        with open(parser_args.json_path, 'r', encoding='utf-8') as json_file:
            books = json.load(json_file)
    except FileNotFoundError as error:
        sys.exit(f'Неверно указан путь или имя файлаю Ошибка {error}')

    template = env.get_template('template.html')

    for book in books:
        book['book_path'] = parse.quote(book['book_path'], safe='/')  # заменяем в пути пробелы

    Path(PAGES_DIRECTORY).mkdir(parents=True, exist_ok=True)
    books = list(chunked(books, BOOK_CARDS_PER_PAGE))
    for page_number, books_page in enumerate(books):
        rendered_page = template.render(
            books=books[page_number],
            pages_number=len(books),
            page_number=page_number
        )
        with open(Path(PAGES_DIRECTORY).joinpath(f'index{page_number+1}.html'), 'w', encoding="utf8") as file:
            file.write(rendered_page)


def main():
    on_reload()
    server = Server()
    server.watch('template.html', on_reload)
    server.serve(root='.')


if __name__ == '__main__':
    main()
