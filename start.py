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
from datetime import datetime

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


def get_campaign_stats():
    """
    Fetch campaign stats from redis cache
    :return:
    """
    today_data = datetime.now().strftime("%Y-%m-%d")
    redis_client = redis.StrictRedis(host="rtb-cache.r1kpgb.ng.0001.usw2.cache.amazonaws.com")
    fm_wins = redis_client.get("win_70848460555_" + today_data)
    fm_spend = redis_client.get("budget_70848460555_" + today_data)
    ebay_wins = redis_client.get("win_67361349506_" + today_data)
    ebay_spend = redis_client.get("budget_67361349506_" + today_data)
    data = [
        {
            "name": "FM",
            "wins": fm_wins.decode("utf-8"),
            "spend": fm_spend.decode("utf-8")
        },
        {
            "name": "Ebay",
            "wins": ebay_wins.decode("utf-8"),
            "spend": ebay_spend.decode("utf-8")
        }
    ]
    return data

@socketio.on('queues_latest', namespace='/hello')
def latest_queues():
    """
    Fetching latest data
    :return:
    """
    print('client requested latest queues data')
    data = get_campaign_stats()
    # data = [{"name": "FM", "spend": time.time()+1, "wins": time.time()+2},
    # {"name": "FM", "spend": time.time()+3, "wins": time.time()+4}]
    emit('queues_data_push', data)


def emit_queues():
    """
    Send latest data to client
    :return:
    """
    data = get_campaign_stats()
    # data = [{"name": "FM", "spend": time.time()+1, "wins": time.time()+2},
    # {"name": "FM", "spend": time.time()+3, "wins": time.time()+4}]
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
            time.sleep(2)
            emit_queues()
    thready = Thread(target=scheduler_loop)
    thready.daemon = True
    thready.start()


if __name__ == '__main__':
    start_scheduler()
    socketio.run(app, host='0.0.0.0', port=5000)
