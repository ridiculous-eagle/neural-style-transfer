from gevent import pywsgi
import gevent, app, logging.config, os, json


with open("logging.cfg", "r") as stream:
    logging_config = json.load(stream)
logging.config.dictConfig(logging_config)
logger = logging.getLogger(__name__)
try:
    logger.info("Start Serving at 21050")
    http_server = pywsgi.WSGIServer(('0.0.0.0', 21050), app.flask_app)
    http_server.serve_forever()
except Exception as ex:
    logger.error(ex)
    exit(-1)
