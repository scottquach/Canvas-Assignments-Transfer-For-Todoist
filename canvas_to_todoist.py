import requests
import json
from todoist.api import TodoistAPI
from requests.auth import HTTPDigestAuth

api_file = open("C:\\Users\\Scott Quach\\Desktop\\Python Stuff\\api_keys.txt")
keys = api_file.readlines()
api_file.close()
print(keys[0])
print(keys[1])

canvas_api_heading = 'https://canvas.instructure.com'
canvas_token = keys[0]

#Initialize TodoistAPI
todoist_api_token = keys[1]
todoist_api = TodoistAPI(todoist_api_token)
todoist_api.reset_state()
todoist_api.sync()

#Course ID of the current courses I'm taking
css_342_id = 100000001130860
css_301_id = 100000001130859
css_360_id = 100000001215804

course_name_id_dict = {
                        'CSS 342 Data Structures and Algorithms': css_342_id,
                        'CSS 301 Technical Writing': css_301_id,
                        'CSS 360 Software Engineering': css_360_id}
course_id_name_dict = {
                        css_342_id: 'CSS 342 Data Structures and Algorithms',
                        css_301_id: 'CSS 301 Technical Writing',
                        css_360_id: 'CSS 360 Software Engineering'}

header = {"Authorization":"Bearer " + canvas_token}
param = {'per_page': '100', 'include':'submission'}

assignments = []
todoist_tasks = []
todoist_project_dict = {}

# Iterates over the course_name_id_dict and loads all of the users assignments
# for those classes. Appends assignment objects to assignments list
def load_assignments():
    for course_name in course_name_id_dict:
        response = requests.get(canvas_api_heading + '/api/v1/courses/' +
        str(course_name_id_dict[course_name]) + '/assignments', headers=header,
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
    for course_name in course_name_id_dict:
        if course_name not in todoist_project_dict:
            project = todoist_api.projects.add(course_name)
            todoist_api.commit();
            todoist_api.sync()

            todoist_project_dict[project['name']] = project['id']
        else:
            print("the key was in dict, don't create project")

# Transfers over assignments from canvas over to Todoist, the method Checks
# to make sure the assignment has not already been trasnfered to prevent overlap
def transfer_assignments_to_todoist():
    for assignment in assignments:
        course_name = course_id_name_dict[assignment['course_id']]
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

# load_todoist_projects()
# load_assignments()
# load_todoist_tasks()
#
# create_todoist_projects()
#
# transfer_assignments_to_todoist()
