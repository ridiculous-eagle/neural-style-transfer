from gevent import pywsgi
import gevent, app

print('Start Serving...')
http_server = pywsgi.WSGIServer(('0.0.0.0', 5000), app.flask_app)
http_server.serve_forever()
