import configparser
import os

from flask import request, abort
from flask_restplus import Namespace, Resource
from linebot import WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent,
    TextMessage,
)

import line.in_event

api = Namespace('line-webhook', description='Line Webhook')

cur_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(os.path.dirname(cur_dir), 'config.ini')
config = configparser.ConfigParser()
config.read(config_path)

handler = WebhookHandler(config['LINE']['ChannelSecret'])


@api.route('/test')
class TestCallback(Resource):
    def get(self):
        print('/test')
        return 'Hello'


@api.route('/')
class Callback(Resource):
    def post(self):
        # get X-Line-Signature header value
        signature = request.headers['X-Line-Signature']
        # get request body as text
        body = request.get_data(as_text=True)
        print(body)
        # handle webhook body
        try:
            handler.handle(body, signature)
        except InvalidSignatureError:
            abort(400)
        return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    in_event = line.in_event.TextMessage()
    in_event.core(event=event)
