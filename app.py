from flask import Flask, render_template, request, url_for, flash, redirect, abort
from flask_sqlalchemy import SQLAlchemy
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

def get_db_connection():
    conn = sqlite3.connect('main.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_entry(entry_id):
    conn = get_db_connection()
    entries = conn.execute('SELECT * FROM entries WHERE id = ?', (entry_id,)).fetchone()
    conn.close()
    if entries is None:
        abort(404)
    return entries

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'
db = SQLAlchemy(app)

@app.route('/')
def index():
    conn = get_db_connection()
    entries = conn.execute('SELECT * FROM entries').fetchall()
    conn.close()
    return render_template('index.html', entries=entries)

@app.route('/create/', methods=('GET', 'POST'))
def create():
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
    return render_template('create.html')

@app.route('/<int:id>/edit/', methods=('GET', 'POST'))
def edit(id):
    entry = get_entry(id)

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

    return render_template('edit.html', entry=entry)

@app.route('/<int:id>/delete/', methods=('GET',))
def delete(id):
    entry = get_entry(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM entries WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('"Entry No. {}" was successfully deleted!'.format(entry['number']), 'info')
    return redirect(url_for('index'))

app.run(debug=True)


class Entries(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  number = db.Column(db.Integer(19), unique=False, nullable=False)
  datetime = db.Column(db.String(19), unique=False, nullable=False)
  isExit = db.Column(db.Bool(19), unique=False, nullable=False)
  gender = db.Column(db.String(1), unique=False, nullable=False)

  def __repr__(self):
        return f'<Entity {self.id}, {self.number}, {self.datetime}, {self.isExit}, {self.gender}>'