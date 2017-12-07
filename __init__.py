import json
import logging

with open('config.json', 'r') as config_file:
    logging_config = dictConfig(json.load(config_file)['logging'])