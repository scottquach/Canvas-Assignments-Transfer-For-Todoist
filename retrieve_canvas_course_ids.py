import requests

with open("api_keys.txt") as api_file:
    keys = api_file.readlines()

canvas_api_heading = 'https://canvas.instructure.com'
canvas_token = keys[1].strip()

header = {'Authorization': 'Bearer ' + canvas_token}
param = {'per_page': 100}

def load_courses(should_print):
    response = requests.get(canvas_api_heading + '/api/v1/courses',
         headers=header, params=param)

    courses_id_name_dict = {}

    for course in response.json():
        courses_id_name_dict[course.get('id', None)] = course.get('name', None)
        if should_print:
            if course.get('name') != None:
                print(course.get('name') + ': ' + str(course.get('id', "")))
    return courses_id_name_dict

load_courses(True)
