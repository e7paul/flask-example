# импорт зависимостей
from flask import Flask, render_template, request, url_for, flash, redirect, abort
from flask_sqlalchemy import SQLAlchemy
import sqlite3

# инициализация приложения
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'

# получить соединение с БД
def get_db_connection():
    conn = sqlite3.connect('main.db')
    conn.row_factory = sqlite3.Row
    return conn

# получить запись по ID
def get_entry(entry_id):
    conn = get_db_connection()
    entries = conn.execute('SELECT * FROM entries WHERE id = ?', (entry_id,)).fetchone()
    conn.close()
    if entries is None:
        abort(404)
    return entries

# получить данные таблицы genders
def get_genders():
    conn = get_db_connection()
    genders = conn.execute('SELECT * FROM genders').fetchall()
    conn.close()
    if genders is None:
        abort(404)
    return genders

# инициализация соединения с БД
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'
db = SQLAlchemy(app)

# маршрут для просмотра
@app.route('/')
def index():
    conn = get_db_connection()
    entries = conn.execute('SELECT entries.id, entries.number, entries.datetime, entries.isExit, genders.name as gender FROM entries INNER JOIN genders on genders.id = entries.gender').fetchall()
    conn.close()
    return render_template('index.html', entries=entries)

# маршрут для создания
@app.route('/create/', methods=('GET', 'POST'))
def create():
    genders = get_genders()
    if request.method == 'POST':
        number = request.form.get('number', '')
        datetime = request.form.get('datetime', '')
        isExit = int(request.form.get('isExit', 0))
        gender = request.form.get('gender', '')

        if not number:
            flash('number is required!', 'error')
        elif not datetime:
            flash('datetime is required!', 'error')
        elif not gender:
            flash('gender is required!', 'error')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO entries (number, datetime, isExit, gender) VALUES (?, ?, ?, ?)',
                         (number, datetime, isExit, gender))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))
    return render_template('create.html', genders=genders)

# маршрут для редактирования
@app.route('/<int:id>/edit/', methods=('GET', 'POST'))
def edit(id):
    entry = get_entry(id)
    genders = get_genders()

    if request.method == 'POST':
        number = request.form.get('number', '')
        datetime = request.form.get('datetime', '')
        isExit = int(request.form.get('isExit', 0))
        gender = request.form.get('gender', '')

        if not number:
            flash('number is required!', 'error')
        elif not datetime:
            flash('datetime is required!', 'error')
        elif not gender:
            flash('gender is required!', 'error')
        else:
            conn = get_db_connection()
            conn.execute('UPDATE entries SET number = ?, datetime = ?, isExit = ?, gender = ? WHERE id = ?',
                (number, datetime, isExit, gender, id))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('edit.html', entry=entry, genders=genders)

# маршрут для удаления
@app.route('/<int:id>/delete/', methods=('GET',))
def delete(id):
    entry = get_entry(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM entries WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('"Entry No. {}" was successfully deleted!'.format(entry['number']), 'info')
    return redirect(url_for('index'))

# старт приложения в режиме debug
app.run(debug=True)

