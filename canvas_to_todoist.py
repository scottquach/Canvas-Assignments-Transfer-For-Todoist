import requests
import json
from todoist.api import TodoistAPI
from requests.auth import HTTPDigestAuth
from retrieve_canvas_course_ids import load_courses

with open("C:\\Users\\Scott Quach\\Desktop\\Python Stuff\\api_keys.txt") as api_file:
    keys = api_file.readlines()

#Initialize TodoistAPI
todoist_api_token = keys[0].strip()
todoist_api = TodoistAPI(todoist_api_token)
todoist_api.reset_state()
todoist_api.sync()

canvas_api_heading = 'https://canvas.instructure.com'
canvas_token = keys[1].strip()

courses_id_name_dict = load_courses(False)
# course_name_id_dict = {v:k for k,v in course_id_name_dict.items()}

course_ids = []
for course_id in keys[2:]:
    course_ids.append(int(course_id.strip()))

header = {"Authorization":"Bearer " + canvas_token}
param = {'per_page': '100', 'include':'submission'}

assignments = []
todoist_tasks = []
todoist_project_dict = {}

# Iterates over the course_name_id_dict and loads all of the users assignments
# for those classes. Appends assignment objects to assignments list
def load_assignments():
    for course_id in course_ids:
        response = requests.get(canvas_api_heading + '/api/v1/courses/' +
        str(course_id) + '/assignments', headers=header,
        params=param)

        for assignment in response.json():
            assignments.append(assignment)

# Loads all user tasks from Todoist
def load_todoist_tasks():
    tasks = todoist_api.state['items']
    for task in tasks:
        todoist_tasks.append(task)

# Loads all user projects from Todoist
def load_todoist_projects():
    projects = todoist_api.state['projects']
    for project in projects:
        todoist_project_dict[project['name']] = project['id']
    # print(todoist_project_dict)

# Checks to see if the user has a project matching their course names, if there
# isn't a new project will be created
def create_todoist_projects():
    for course_id in course_ids:
        if courses_id_name_dict[course_id] not in todoist_project_dict:
            project = todoist_api.projects.add(courses_id_name_dict[course_id])
            todoist_api.commit();
            todoist_api.sync()

            todoist_project_dict[project['name']] = project['id']
        else:
            print("the key was in dict, don't create project")

# Transfers over assignments from canvas over to Todoist, the method Checks
# to make sure the assignment has not already been trasnfered to prevent overlap
def transfer_assignments_to_todoist():
    for assignment in assignments:
        course_name = courses_id_name_dict[assignment['course_id']]
        assignment_name = assignment['name']
        project_id = todoist_project_dict[course_name]

        is_synced = False
        for task in todoist_tasks:
            if task['content'] == (assignment_name + ' Due') and \
            task['project_id'] == project_id:
                print("Assignment already synced: " + assignment['name'])
                is_synced = True

        if not is_synced:
            if assignment['submission']['submitted_at'] == None:
                print("Adding assignment " + assignment['name'])
                add_new_task(assignment, project_id)
            else:
                print("assignment already submitted " + assignment['name'])
        else:
            print("assignmentt already synced")
    todoist_api.commit()

# Adds a new task from a Canvas assignment object to Todoist under the
# project coreesponding to project_id
def add_new_task(assignment, project_id):
    test_task = todoist_api.items.add(assignment['name'] + ' Due', project_id,
    date_string=assignment['due_at'])

load_todoist_projects()
load_assignments()
load_todoist_tasks()

create_todoist_projects()

transfer_assignments_to_todoist()
