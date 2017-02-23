from mainapp import app
from flask_cors import CORS, cross_origin

print 'Game backend by Ronan'

app.config.from_object('configuration.BaseConfig')
CORS(app, supports_credentials = True)
app.run(host='0.0.0.0', debug=True)


