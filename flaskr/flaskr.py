import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash

# create our little application :)
app = Flask(__name__)

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'flaskr.db'),
    DEBUG=True,
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)


def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


def init_db():
    """Initializes the database."""
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()


@app.cli.command('initdb')
def initdb_command():
    """Creates the database tables."""
    init_db()
    print('Initialized the database.')


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


@app.route('/')
def show_entries():
    db = get_db()
    cur = db.execute('select title, author, text from entries order by id desc')
    entries = cur.fetchall()
    return render_template('show_entries.html', entries=entries)


@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    db = get_db()
    db.execute('insert into entries (title, author, text) values (?, ?, ?)',
               [request.form['title'], session['username'], request.form['text']])
    db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    db = get_db()
    cur = db.cursor()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cur.execute('''select password from users where username = '{}'
                    '''.format(username))
        result = cur.fetchall()
        if not result:
            error = 'This user does not exist'
        else:
            real_password = result[0][0]
            if str(password) == str(real_password):
                session['logged_in'] = True
                session['username'] = username
                flash('You were logged in')
                return redirect(url_for('show_entries'))
            else:
                error = 'Invalid password'
    return render_template('login.html', error=error)

@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        user_name = request.form['username']
        email = request.form['email']
        password = request.form['password']
        db = get_db()
        try:
            db.execute('insert into users (username, password, email) values \
                       (?, ?, ?)', (user_name, password, email))
            db.commit()
            flash('Register Success!')
            return redirect(url_for('login'))
        except:
            error = 'The user already exists'
    return render_template('register.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))

@app.route('/manage', methods=['GET', 'POST'])
def manage():
    if request.method == 'POST':
        if request.form['manage_action'] == 'Flush_All_Articles':
            db = get_db()
            db.execute('delete from entries ')
            db.commit()
            flash('Flush All Articles')
        elif request.form['manage_action'] == 'Flush_All_Users':
            db = get_db()
            db.execute('delete from users ')
            db.commit()
            flash('Flush All Users')
    return render_template('manage.html')


if __name__ == '__main__':  
    app.run(host="0.0.0.0", port=80)
  
