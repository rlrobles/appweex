from flask import Flask, url_for
#from werkzeug.serving import run_simple
#from werkzeug.wsgi import DispatcherMiddleware



#app.debug = True
#app.wsgi_app = PrefixMiddleware(app.wsgi_app, prefix='/foo')

app = Flask(__name__)
app.config['APPLICATION_ROOT'] = '/abc/123'
#app.config["APPLICATION_ROOT"] = 'appweex'
#app.register_blueprint(app, url_prefix='appweex')
#app.wsgi_app = PrefixMiddleware(app.wsgi_app, prefix='/foo')
#app.route = prefix_route(app.route, '/your_prefix')

import weexConstants
basePath = weexConstants.PATH_APPLICATION

@app.route(basePath + '/')
def index():
    return "Hello World!"

if __name__ == '__main__':
   app.run(debug = True)