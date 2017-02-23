class BaseConfig(object):
       'Base config class'
       SECRET_KEY = open('./SECRET_KEY').read()
       DEBUG = True

class ProdConfig(BaseConfig):
       'Production config class'
       DEBUG = False