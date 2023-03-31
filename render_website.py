import json

from urllib import parse
from more_itertools import chunked
from jinja2 import Environment, FileSystemLoader, select_autoescape
from pathlib import Path
from livereload import Server


PAGE_DIRECTORY = 'pages'


def on_reload():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')

    with open(Path('media').joinpath('about_books.json'), 'r', encoding='utf-8') as json_file:
        books = json.load(json_file)

    for book in books:
        book['book_path'] = parse.quote(book['book_path'], safe='/')  # заменяем в пути пробелы

    Path(PAGE_DIRECTORY).mkdir(parents=True, exist_ok=True)
    books = list(chunked(books, 40))
    for page_number, books_page in enumerate(books):
        rendered_page = template.render(
            books=books[page_number],
            pages_number=len(books),
            page_number=page_number
        )
        with open(Path(PAGE_DIRECTORY).joinpath(f'index{page_number+1}.html'), 'w', encoding="utf8") as file:
            file.write(rendered_page)


def main():
    on_reload()
    server = Server()
    server.watch('template.html', on_reload)
    server.serve(root='.')


if __name__ == '__main__':
    main()
