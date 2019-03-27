from flask import Flask, request, render_template, redirect
from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, validators, SubmitField, TextAreaField, PasswordField, FieldList, SelectField
from wtforms.validators import DataRequired
from bookDB import *


class ViewBookForm(FlaskForm):  # форма просмотра описания книги
    title = StringField('Название книги', validators=[DataRequired()])
    author = StringField('Автор книги', validators=[DataRequired()])
    genre = SelectField(u'Жанр', choices=[('1', 'Проза'), ('2', 'Поэзия'), ('3', 'Фантастика'), ('4', 'Приключения'),
                                            ('5', 'История'), ('6', 'Мемуары'), ('0', 'Неизвестно')])
    year = StringField('Год написания')
    description = TextAreaField('Описание')
    content = TextAreaField('Часть текста')
    link = StringField('Ссылка на файл книги')


class AddFileBookForm(FlaskForm):  # форма добавления файла с текстом книги
    submit = SubmitField('Добавить')


class AddBookForm(ViewBookForm):  # форма добавления описания книги(наследуется от ViewBookForm)
    submit = SubmitField('Добавить')


class ModifyBookForm(ViewBookForm):    # форма изменения описания книги(наследуется от ViewBookForm)
    submit = SubmitField('Сохранить')


class LoginForm(FlaskForm):  # форма входа в систему
    username = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')


class RegisterForm(FlaskForm):  # форма регистрации
    username = StringField('Логин', validators=[DataRequired()])
    email = StringField('Почта')
    password = PasswordField('Пароль', validators=[DataRequired()])
    accept_rules = BooleanField('Я согласен с правилами сайта', [validators.InputRequired()])
    submit = SubmitField('Зарегистрироваться')


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route('/view_book/<int:book_id>', methods=['GET'])  # страница просмотра описания книги
def view_book(book_id):
    form = ViewBookForm()
    book = books.get(book_id)
    form.title.data = book[1]
    form.author.data = book[2]
    form.genre.data = book[3]
    form.year.data = book[8]
    form.description.data = book[4]
    form.content.data = book[5]
    form.link.data = book[6]
    return render_template('view_book.html', title='Просмотр книги', form=form, ssn=ssn, view=1)


@app.route('/modify_book/<int:book_id>', methods=['GET', 'POST'])  # страница изменения описания книги
def modify_book(book_id):
    form = ModifyBookForm()
    if request.method == 'GET':
        book = books.get(book_id)
        form.title.data = book[1]
        form.author.data = book[2]
        form.genre.data = book[3]
        form.year.data = book[8]
        form.description.data = book[4]
        form.content.data = book[5]
        form.link.data = book[6]
    elif request.method == 'POST':
        title = form.title.data
        author = form.author.data
        genre = form.genre.data
        year = form.year.data
        description = form.description.data
        content = form.content.data
        link = form.link.data
        books.update(title, author, genre, description, content, link, ssn['user_id'], year, book_id)
        return redirect("/index")
    return render_template('add_book.html', title='Изменение книги', form=form, ssn=ssn, view=0)


@app.route('/add_book', methods=['GET', 'POST'])  # страница добавления книги
def add_book():
    form = AddBookForm()
    exist = 0
    if form.validate_on_submit():
        title = form.title.data
        author = form.author.data
        if books.exist_book(title, author):
            exist = 1
        else:
            genre = form.genre.data
            year = form.year.data
            description = form.description.data
            content = form.content.data
            link = form.link.data
            books.insert(title, author, genre, description, content, link, ssn['user_id'], year)
            return redirect("/index")
    return render_template('add_book.html', title='Новая книга', form=form, ssn=ssn, view=0, exist=exist)


@app.route('/add_file_book/<int:book_id>', methods=['GET', 'POST'])  # страница добавления файла книги
def add_file_book(book_id):
    form = AddFileBookForm()
    if request.method == 'POST':
        try:
            f = request.files['file']
            with open("books/" + f.filename, 'wb') as file:
                file.write(f.read())
            books.update_link(f.filename, book_id)
            return redirect("/index")
        except Exception:
            return "Произошла ошибка"
    return render_template('add_file_book.html', title='Выгрузка файла книги', form=form, ssn=ssn, view=0)


@app.route('/del_book/<int:book_id>', methods=['GET', 'POST'])  #удаление книги
def del_book(book_id):
    books.delete(book_id)
    return redirect("/index")


@app.route('/')  # стартовая страница со списком книг
@app.route('/index')
def index():
    return render_template('index.html', ssn=ssn, books=books.get_all())


@app.route('/login', methods=['GET', 'POST'])  # страница входа в систему
def login():
    form = LoginForm()
    status=0
    if form.validate_on_submit():
        user_name = form.username.data
        password = form.password.data
        exists = users.exists(user_name, password)
        if exists[0]:
            if exists[1][3] == 0:  # проверка, не заблокирован ли пользователь
                ssn['username'] = user_name
                ssn['user_id'] = exists[1][0]
                ssn['level'] = exists[1][5]
                return redirect("/index")
            else:
                status = 2
        else:
            status = 1
    return render_template('login.html', title='Авторизация', form=form, status=status)


@app.route('/register', methods=['GET', 'POST'])  # страница регистрации нового пользователя
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user_name = form.username.data
        email = form.email.data
        password = form.password.data
        if not users.existUser([user_name]):
            users.insert(user_name, email, password)
            exists = users.exists(user_name, password)
            ssn['username'] = user_name
            ssn['user_id'] = exists[1][0]
            ssn['level'] = exists[1][5]
            return redirect("/index")
        else:
            return render_template('register.html', title='Регистрация', form=form, exist=True)
    return render_template('register.html', title='Регистрация', form=form, exist=False)


@app.route('/logout')  # страница выхода из системы
def logout():
    ssn.pop('username',0)
    ssn.pop('user_id',0)
    ssn.pop('level',0)
    return redirect('/index')


@app.route('/lock_user/<int:user_id>')  # блокировка и снятие блокировки пользователя
def lock_user(user_id):
    state = users.get(user_id)
    users.lock(user_id, 1 - state[3])
    return redirect("/user_list")


@app.route('/user_list')  # страница со списком пользователей
def user_list():
    # print(users.get_all())
    return render_template('user_list.html', ssn=ssn, users=users.get_all())


if __name__ == '__main__':
    db = DB()
    ssn = {}
    users = UsersModel(db.get_connection())
    users.init_table()
    books = BooksModel(db.get_connection())
    books.init_table()
    # journals = JournalsModel(db.get_connection())
    # journals.init_table()
    app.run(port=8080, host='127.0.0.1')
