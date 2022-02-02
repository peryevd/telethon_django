import configparser

INI_FILE = "config.ini"
config = configparser.ConfigParser()
config.sections()
config.read(INI_FILE)
api_id = config['TELEGRAM']['API_ID']
api_hash = config['TELEGRAM']['API_HASH']

username = config['TELEGRAM']['USERNAME']