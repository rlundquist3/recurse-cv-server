import asyncio
import json
import os
import time
from urllib.parse import urlencode
from dotenv import load_dotenv
from actioncable.connection import Connection
from actioncable.subscription import Subscription
from . import osc

HOST = 'recurse.rctogether.com'

async def listen():
    load_dotenv()
    app_id = os.getenv("RC_APP_ID")
    app_secret = os.getenv("RC_APP_SECRET")
    query = urlencode({'app_id': app_id, 'app_secret': app_secret})

    connection = Connection(
        url='wss://{}/cable?{}'.format(HOST, query),
        origin='https://{}'.format(HOST),
    )
    connection.connect()

    subscription = Subscription(connection, identifier={'channel': 'ApiChannel'})
    subscription.on_receive(callback=handle_message)
    subscription.create()

    print('Listening... press Ctrl+C to quit.')
    try:
        await asyncio.Future()
    finally:
        connection.disconnect()

def handle_message(message):
    if message['type'] == 'entity':
        payload = message['payload']
        entity_type = payload['type']

        match entity_type:
            case 'Avatar':
                print(f"event for {payload['person_name']}")
                osc.send_message(1, 1)
            case 'Bot':
                print(f"event for {payload['name']}")
                osc.send_message(2, 1)

        """
        TODO: figure out potentially interesting ways to combine the data to send various CV
        """
        # name = get_name(payload=payload)
        # batch = payload['flair'] if 'flair' in payload else ''
        # direction = payload['direction']
        # position = payload['pos']
