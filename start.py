"""
Prototype for Real time Stats view
"""

#import eventlet
#eventlet.monkey_patch()
import time
from threading import Thread
from pymongo import MongoClient
from flask import Flask, render_template
from bson.json_util import dumps
from flask_socketio import SocketIO, emit, join_room
import redis

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
# socketio = SocketIO(app)
# The below line works, but is not what I want. I need to use eventlet
socketio = SocketIO(app, async_mode='threading')


@app.route('/')
@app.route('/home')
def index():
    """
    Home page
    :return: Template for home page
    """
    return render_template('index.html')


@app.route('/login')
def login():
    """
    Login page view
    :return:
    """
    return render_template('login.html')


@app.route('/register')
def register():
    """
    Register page view
    :return:
    """
    return render_template('register.html')


@app.route('/forgot-password')
def forget_password():
    """
    Forgot password page
    :return:
    """
    return render_template('forgot-password.html')


@app.route('/dashboard')
def dashboard():
    """
    Dashboard
    :return:
    """
    return render_template('dashboard.html')


@socketio.on('connect', namespace='/hello')
def sys_connect():
    """
    Socket connection
    :return:
    """
    print('client connected')


@socketio.on('join', namespace='/hello')
def join(message):
    """
    Joining socket room
    :param message:
    :return:
    """
    join_room(message['room'])
    print('client joined room %s' % message['room'])


@socketio.on('queues_latest', namespace='/hello')
def latest_queues():
    """
    Fetching latest data
    :return:
    """
    print('client requested latest queues data')
    client = MongoClient()
    db_client = client.company
    employeeslist = db_client.employees
    data = dumps(employeeslist.find())
    emit('queues_data_push', data)


def emit_queues():
    """
    Send latest data to client
    :return:
    """
    redis_client = redis.StrictRedis(host="rtb-cache.r1kpgb.ng.0001.usw2.cache.amazonaws.com")
    wins = redis_client.get("win_70848460555_2019-08-06")
    spend = redis_client.get("budget_70848460555_2019-08-06")
    data = {"name": "FM", "spend": spend, "wins": wins}
    socketio.emit('queues_data_push', data, namespace='/hello', room='queues')


def start_scheduler():
    """
    scheduler
    :return:
    """
    def scheduler_loop():
        """
        Scheduler loop
        :return:
        """
        while True:
            time.sleep(1)
            emit_queues()
    thready = Thread(target=scheduler_loop)
    thready.daemon = True
    thready.start()


if __name__ == '__main__':
    start_scheduler()
    socketio.run(app)
