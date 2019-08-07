"""
Prototype for Real time Stats view
"""

# Local libraries
import time
import os
import json
from threading import Thread

# Third party libraries
import requests
from flask import Flask, render_template
from flask_socketio import SocketIO, emit, join_room

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(12)
socket_io = SocketIO(app, async_mode='threading')


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


@socket_io.on('connect', namespace='/hello')
def sys_connect():
    """
    Socket connection
    :return:
    """
    print('client connected')


@socket_io.on('join', namespace='/hello')
def join(message):
    """
    Joining socket room
    :param message:
    :return:
    """
    join_room(message['room'])
    print('client joined room %s' % message['room'])


def fetch_api(url):
    """
    Make an API call to tracking servers to get tracking details
    :param url:
    :return:
    """
    data = requests.get(url)
    response_data = json.loads(data.content)
    if response_data["status"] == "success":
        return response_data["response"]
    return {}


def format_campaign_data(campaign_data):
    """
    Function to format campaign data
    :param campaign_data:
    :return:
    """
    new_campaign_data = {
        "name": campaign_data[0],
        "budget_cap": campaign_data[1],
        "budget_spent": campaign_data[2],
        "status": campaign_data[3],
        "bid_cap": campaign_data[4],
        "today_spend": campaign_data[5],
        "wins": campaign_data[6],
        "inbounds": campaign_data[7],
        "ad_ctr": campaign_data[8],
        "conversions": campaign_data[9],
        "conversion_rate": campaign_data[10],
        "cpa": campaign_data[11]
    }
    return new_campaign_data


def get_campaign_stats():
    """
    Fetch campaign stats from redis cache
    :return:
    """
    west_url = "https://offers.expertsaver.net/stats/campaigns"
    east_url = "https://rtbapi.clicksco.com/stats/campaigns"
    west_campaigns_data = fetch_api(west_url)
    east_campaigns_data = fetch_api(east_url)
    both_regions_data = {}
    west_campaigns_data_new = {}
    east_campaigns_data_new = {}
    for key in west_campaigns_data:
        # print(west_campaigns_data[key][3])
        if west_campaigns_data[key][3] == "1":  # Check if the campaign is active or not
            final_record = {}
            east_record = format_campaign_data(east_campaigns_data.get(key, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]))
            west_record = format_campaign_data(west_campaigns_data.get(key, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]))
            west_campaigns_data_new[key] = west_record
            east_campaigns_data_new[key] = east_record
            final_record["name"] = west_record["name"]
            final_record["today_spend"] = round(west_record["today_spend"] + east_record["today_spend"], 6)
            final_record["wins"] = west_record["wins"] + east_record["wins"]
            final_record["inbounds"] = west_record["inbounds"] + east_record["inbounds"]
            final_record["ad_ctr"] = round((west_record["ad_ctr"] + east_record["ad_ctr"])/2, 3)
            final_record["conversions"] = west_record["conversions"] + east_record["conversions"]
            final_record["conversion_rate"] = round((west_record["conversion_rate"] + east_record["conversion_rate"])/2, 3)
            final_record["cpa"] = round((west_record["cpa"] + east_record["cpa"])/2, 3)
            both_regions_data[key] = final_record
    campaign_stats = {
        "west_campaigns_data": {
            "stats": west_campaigns_data_new,
            "region": "West Region"
        },
        "east_campaigns_data": {
            "stats": east_campaigns_data_new,
            "region": "East Region"
        },
        "both_regions_data": {
            "stats": both_regions_data,
            "region": "Both Regions"
        }
    }
    return campaign_stats


@socket_io.on('queues_latest', namespace='/hello')
def latest_queues():
    """
    Fetching latest data
    :return:
    """
    print('client requested latest queues data')
    data = get_campaign_stats()
    emit('queues_data_push', data)


def emit_queues():
    """
    Send latest data to client
    :return:
    """
    data = get_campaign_stats()
    socket_io.emit('queues_data_push', data, namespace='/hello', room='queues')


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
            time.sleep(5)
            emit_queues()
    thready = Thread(target=scheduler_loop)
    thready.daemon = True
    thready.start()


if __name__ == '__main__':
    start_scheduler()
    socket_io.run(app, host='0.0.0.0', port=5000)
