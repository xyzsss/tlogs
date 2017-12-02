import os
import sqlite3
import datetime
from flask import Flask, request, g, render_template, \
        redirect, url_for, session, abort, flash 
app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'ftlogs.db'),
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='nimda'
))


def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


@app.route('/debug')
def debug():
    app.logger.error('=================================')
    # app.logger.error(request.headers)
    return 'debug'


@app.route('/404')
def redirect_show():
    return redirect(url_for('index'))


@app.route('/info')
def info_show():
    vagent = request.headers.get('User-Agent')
    vhost = request.headers.get('Host')
    vcookie = request.headers.get('Cookie')
    vaddr = request.remote_addr
    return render_template(
        'info.html', vagent=vagent, vcookie=vcookie, vaddr=vaddr, vhost=vhost)


@app.route('/check_session')
def session_check():
    if 'username' in session:
        return 'Logged in as %s' % (session['username'])
    return 'UNLOGIN'


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404


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


def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

# @app.cli.command('initdb')
# def initdb_command():
#     """Initializes the database."""
#     init_db()
#     print('Initialized the database.')


@app.route('/showlogs')
def logs_show():
    db = get_db()
    cur = db.execute('select context, time, extra from tlog order by id desc limit 15')
    entries = cur.fetchall()
    return render_template('showlogs.html', entries=entries)


@app.route('/add', methods=['POST'])
def log_entry_add():
    db = get_db()
    app.logger.error(request.form['context'])
    print(request.form['extra'])
    db.execute('insert into tlog (context, extra, time) values (?, ?, ?)',
        [request.form['context'], request.form['extra'], datetime.datetime.now()])
    db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('logs_show'))


@app.route('/log')
def log_add():
    return render_template('log.html')


@app.route('/')
def index():
    return render_template('index.html')
