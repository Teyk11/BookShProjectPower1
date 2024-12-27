import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Настройка базы данных
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Модель для хранения данных о книгах
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    price = db.Column(db.String(20), nullable=False)
    availability = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"<Book {self.title}>"

# Функция для парсинга данных с сайта
def scrape_books():
    url = "http://books.toscrape.com/"
    response = requests.get(url)

    # Проверим статус код
    if response.status_code != 200:
        print(f"Ошибка при запросе: {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    books = []

    # Ищем все блоки с книгами
    for book in soup.find_all('article', class_='product_pod'):
        title = book.find('h3').find('a')['title']
        price = book.find('p', class_='price_color').text
        availability = book.find('p', class_='instock availability').text.strip()

        # Проверяем, есть ли книга в базе, чтобы избежать дублирования
        if not Book.query.filter_by(title=title).first():
            new_book = Book(title=title, price=price, availability=availability)
            db.session.add(new_book)
        books.append({
            'title': title,
            'price': price,
            'availability': availability
        })

    db.session.commit()  # Сохраняем изменения в базе данных
    return books

# Главная страница
@app.route('/')
def index():
    books = scrape_books()  # Получаем данные с сайта и сохраняем их в базу
    return render_template('index.html', books=books)  # Отправляем данные в шаблон

# Страница для просмотра данных из базы
@app.route('/books')
def view_books():
    letter = request.args.get('letter')  # Получаем параметр фильтрации
    if letter:
        books = Book.query.filter(Book.title.like(f"{letter}%")).all()
    else:
        books = Book.query.all()  # Получаем все книги из базы
    return render_template('books.html', books=books, letter=letter)

if __name__ == '__main__':
    # Создаем таблицы в базе данных
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)
