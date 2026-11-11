import json
import os
import time
from urllib.parse import urlencode
from dotenv import load_dotenv
from actioncable.connection import Connection
from actioncable.subscription import Subscription

HOST = 'recurse.rctogether.com'

def listen():
    load_dotenv()
    app_id = os.getenv("APP_ID")
    app_secret = os.getenv("APP_SECRET")
    query = urlencode({'app_id': app_id, 'app_secret': app_secret})

    connection = Connection(
        url='wss://{}/cable?{}'.format(HOST, query),
        origin='https://{}'.format(HOST),
    )
    connection.connect()

    subscription = Subscription(connection, identifier={'channel': 'ApiChannel'})
    subscription.on_receive(callback=on_receive)
    subscription.create()

    print('Listening... press Ctrl+C to quit.')
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print('\nDisconnecting...')
    finally:
        connection.disconnect()

def on_receive(message):
    print(json.dumps(message, indent=2), flush=True)

