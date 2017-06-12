import configparser
import json
import os

from flask import request, Response
from flask_restplus import Namespace, Resource

api = Namespace('fb-webhook', description='Facebook Webhook')

cur_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(os.path.dirname(cur_dir), 'config.ini')
config = configparser.ConfigParser()
config.read(config_path)

access_token = config['FB']['ChannelAccessToken']


@api.route('/test')
class TestCallback(Resource):
    def get(self):
        print('/test')
        return "Hello"


@api.route('/')
class Callback(Resource):
    def get(self):
        verify_token = request.args.get('hub.verify_token', '')
        challenge = request.args.get('hub.challenge', '')
        print(challenge)
        if verify_token == access_token:
            resp = Response(request.args["hub.challenge"])
            resp.headers['Content-Type'] = 'text/plain'
            return resp
        else:
            return "Wrong validation", 403

    def post(self):
        # get data from request
        payload = request.get_data()

        # turn payload to json
        json_data = json.loads(payload)
        print(json_data)

        # # extract entry, entry is an array
        entry = json_data['entry']

        # if "messaging" in entry[0]:
        #     messaging = entry[0]["messaging"][0]
        #     # text message handle
        #     if "message" in messaging and "text" in messaging["message"]:
        #         core = CoreFBTextMessage()
        #         core.core(messaging)
        # elif "changes" in entry[0]:
        #     changes = entry[0]["changes"][0]
        #     core = CoreFBLikePage()
        #     core.core(changes)

        return json.dumps({'success': True}), 200
