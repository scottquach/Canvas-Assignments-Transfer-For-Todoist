#Pull Labels from Todoist
from todoist.api import TodoistAPI
import json

global api_key
global todoist_api

print("Please paste your Todoist API Key. To add an API token, go to your Todoist settings and copy the API token listed under the Integrations Tab. Copy the token and paste below when you are done.")
api_key = input(">").strip()

todoist_api = TodoistAPI(api_key)
todoist_api.reset_state()
todoist_api.sync()

labels = todoist_api.state['labels']

for label in labels:
    print(label['name'] + ": " + str(label['id']))