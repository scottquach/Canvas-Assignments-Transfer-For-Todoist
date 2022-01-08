import requests
import re


with open("api_keys.txt") as api_file:
    keys = api_file.readlines()

canvas_api_heading = 'https://canvas.instructure.com'
canvas_token = keys[1].strip()

header = {'Authorization': 'Bearer ' + canvas_token}
param = {'per_page': 100}

def load_courses(should_print):
    if should_print:
        print("Special characters are scrubbed to be compatable with Todoist restrictions")
    # print("header", header);
    response = requests.get(canvas_api_heading + '/api/v1/courses',
         headers=header)
    # print("RESPONSE", response)

    courses_id_name_dict = {}

    for course in response.json():
        # print(course)
        # courses_id_name_dict[course.get('id', None)] = re.sub(r'[^-a-zA-Z._\s]', '', 'test@34x&# hi')
        courses_id_name_dict[course.get('id', None)] = course.get('name', '')
        if should_print:
            if course.get('name') != None:
                print(courses_id_name_dict[course.get('id', None)] + ': ' + str(course.get('id', "")))
    return courses_id_name_dict

load_courses(True)
