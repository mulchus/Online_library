import json
# import collections

# from http.server import HTTPServer, SimpleHTTPRequestHandler
# from environs import Env
from jinja2 import Environment, FileSystemLoader, select_autoescape
from pathlib import Path
from livereload import Server


def on_reload():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')

    books_path = Path.joinpath(Path.cwd().parents[0], 'Book-parser/', 'about_books.json')
    with open(books_path, 'r', encoding='utf-8') as json_file:
        books = json.load(json_file)

    # books_set = collections.defaultdict(list)
    rendered_page = template.render(
        books=books
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

    # server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    # server.serve_forever()


def main():
    on_reload()
    server = Server()
    server.watch('*.html', on_reload)
    server.serve(root='.')


if __name__ == '__main__':
    main()
