from flask_restplus import Api

from .fb_webhook import api as fb_webhook
from .line_webhook import api as line_webhook

api = Api(
    title='Apis',
    version='1.0',
    description='Apis',
    # All API metadatas
)

api.add_namespace(line_webhook)
api.add_namespace(fb_webhook)
