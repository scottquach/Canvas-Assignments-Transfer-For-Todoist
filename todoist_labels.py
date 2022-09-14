#Pull Labels from Todoist
from todoist.api import TodoistAPI
import json

global config
global todoist_api

with open("config.json") as config_file:
        config = json.load(config_file);


todoist_api = TodoistAPI(config['todoist_api_key'].strip())
todoist_api.reset_state()
todoist_api.sync()

labels = todoist_api.state['labels']

for label in labels:
    print(label['name'] + ":" + str(label['id']))