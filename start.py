#import eventlet
#eventlet.monkey_patch()
from threading import Thread
from pymongo import MongoClient
from flask import Flask, render_template
from bson.json_util import dumps
from flask_socketio import SocketIO, send, emit, join_room, leave_room
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
# socketio = SocketIO(app)
# The below line works, but is not what I want. I need to use eventlet
socketio = SocketIO(app, async_mode='threading')


@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/forgot-password')
def forget_password():
    return render_template('forgot-password.html')


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


@socketio.on('connect', namespace='/hello')
def sys_connect():
    print ('client connected')


@socketio.on('join', namespace='/hello')
def join(message):
    join_room(message['room'])
    print ('client joined room %s' % message['room'])


@socketio.on('queues_latest', namespace='/hello')
def latest_queues():
    print('client requested latest queues data')
    client = MongoClient();
    db = client.company
    employeeslist = db.employees
    data = dumps(employeeslist.find())
    emit('queues_data_push', data)


def emit_queues():
    data = {"name": "FM", "spend": time.time(), "wins": time.time()}
    socketio.emit('queues_data_push', data, namespace='/hello', room='queues')


def start_scheduler():
    def scheduler_loop():
        while True:
            time.sleep(1)
            emit_queues()
    thready = Thread(target=scheduler_loop)
    thready.daemon = True
    thready.start()


if __name__ == '__main__':
    start_scheduler()
    socketio.run(app)