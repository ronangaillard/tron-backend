from mainapp import app
from flask_cors import CORS, cross_origin

if __name__ == '__main__':
    try:
        # Development server
        open('./DEVELOPMENT').close()

        print "WARNING RUNNING AS DEVELOPMENT SERVER"
        app.config.from_object('configuration.BaseConfig')
        CORS(app, supports_credentials = True)
        app.run(host='127.0.0.1')

    except:
        # Production server
        print "Running as production server"
        app.config.from_object('configuration.ProdConfig')
        CORS(app, supports_credentials = True)
        app.run(host='0.0.0.0')


