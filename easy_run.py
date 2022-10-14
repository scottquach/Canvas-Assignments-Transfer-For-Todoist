import requests
import re
import json
from todoist.api import TodoistAPI
from requests.auth import HTTPDigestAuth
import datetime

# Loaded configuration files and creates a list of course_ids
config = {}
header = {}
param = {'per_page': '100', 'include':'submission'}
course_ids = []
assignments = []
todoist_tasks = []
courses_id_name_dict = {}
todoist_project_dict = {}

def main():
    print("  ###################################################")
    print(" #     Canvas-Assignments-Transfer-For-Todoist     #")
    print("###################################################\n")
    initialize_api()
    print("API INITIALIZED")
    select_courses()
    print("Working...")
    load_todoist_projects()
    load_assignments()
    load_todoist_tasks()
    create_todoist_projects()
    transfer_assignments_to_todoist()
    print("Done!")

#Function for Yes/No response prompts during setup
def yes_no(question: str) -> bool:
    reply = None
    while reply not in ("y", "n"):
        reply = input(f"{question} (y/n): ").lower()
    return (reply == "y")

# Makes sure that the user has their api keys and canvas url in the config.json
def initialize_api():
    global config
    global todoist_api

    try:
        with open("config.json") as config_file:
            config = json.load(config_file)
    except FileNotFoundError:
        print("File not Found, running Initial Configuration")
        initial_config()

    #create todoist_api object globally
    todoist_api = TodoistAPI(config['todoist_api_key'].strip())
    todoist_api.reset_state()
    todoist_api.sync()
    header.update({"Authorization":"Bearer " + config['canvas_api_key'].strip()})

def initial_config():
    print("Your Todoist API key has not been configured. To add an API token, go to your Todoist settings and copy the API token listed under the Integrations Tab. Copy the token and paste below when you are done.")
    config['todoist_api_key'] = input(">")
    print("Your Canvas API key has not been configured. To add an API token, go to your Canvas settings and click on New Access Token under Approved Integrations. Copy the token and paste below when you are done.")
    config['canvas_api_key'] = input(">")
    defaults = yes_no("Use default options? (enter no for advanced config)")
    if defaults == True:
        config['canvas_api_heading'] = "https://canvas.instructure.com"
        config['todoist_task_priority'] = 1
        config['todoist_task_label_id'] = []
        config['sync_null_assignments'] = True
        config['sync_locked_assignments'] = True
        config['sync_no_due_date_assignments'] = True
    if defaults == False:   
        custom_url = yes_no("Use default Canvas URL? (https://canvas.instructure.com)")
        if custom_url == True:
            config['canvas_api_heading'] = "https://canvas.instructure.com"
        if custom_url == False:
            print("Enter your custom Canvas URL: (example https://university.instructure.com)")
            config['canvas_api_heading'] = input(">")
        advance_setup = yes_no("Configure Advanced Options? (enter no for default config)")
        if advance_setup == True:
            print("Specify the task priority (1=Priority 4, 2=Priority 3, 3=Priority 2, 4=Priority 1. (Default Priority 4)")
            config['todoist_task_priority'] = int(input(">"))
            print("Enter any Label IDs that you would like assigned to the tasks, separated by comma (pull using todoist_labels.py)")
            config['todoist_task_label_id'] = str("["+input(">")+"]")
            null_assignments = yes_no("Sync not graded/not submittable assignments?")
            config['sync_null_assignments'] = null_assignments
            locked_assignments = yes_no("Sync locked assignments?")
            config['sync_locked_assignments'] = locked_assignments
            no_due_date_assignments = yes_no("Sync assignments with no due date?")
            config['sync_no_due_date_assignments'] = no_due_date_assignments
            
        else:
            config['todoist_task_priority'] = 1
            config['todoist_task_label_id'] = []
            config['sync_null_assignments'] = True
            config['sync_locked_assignments'] = True
            config['sync_no_due_date_assignments'] = True
    config['courses'] = []
    with open("config.json", "w") as outfile:
        json.dump(config, outfile)

# Allows the user to select the courses that they want to transfer while generating a dictionary
# that has course ids as the keys and their names as the values
def select_courses():
    global config

    response = requests.get(config['canvas_api_heading'] + '/api/v1/courses',
            headers=header, params=param)
    if response.status_code == 401:
        print('Unauthorized; Check API Key')
        exit()

    if config['courses']:
        use_previous_input = input("You have previously selected courses. Would you like to use the courses selected last time? (y/n) ")
        print("")
        if use_previous_input == "y" or use_previous_input == "Y":
            for course_id in config['courses']:
                # print(course_id)
                course_ids.append(int(course_id))
            for course in response.json():
                courses_id_name_dict[course.get('id', None)] = re.sub(r'[^-a-zA-Z0-9._\s]', '', course.get('name', ''))
            return

    # If the user does not choose to use courses selected last time
    i = 1
    for course in response.json():
        courses_id_name_dict[course.get('id', None)] = re.sub(r'[^-a-zA-Z0-9._\s]', '', course.get('name', ''))
        if course.get('name') != None:
            print(str(i) + ") " + courses_id_name_dict[course.get('id', "")]  + ': ' + str(course.get('id', "")))
        i+=1
    print("\nEnter the courses you would like to add to Todoist by entering the numbers of the items you would like to select. Separate numbers with spaces.")
    my_input = input(">")
    input_array = my_input.split()
    for item in input_array:
        course_ids.append(response.json()[int(item)-1].get('id', None))

    #write course ids to config.json
    config['courses'] = course_ids
    with open("config.json", "w") as outfile:
        json.dump(config, outfile)

# Iterates over the course_ids list and loads all of the users assignments
# for those classes. Appends assignment objects to assignments list
def load_assignments():
    for course_id in course_ids:
        response = requests.get(config['canvas_api_heading'] + '/api/v1/courses/' +
        str(course_id) + '/assignments', headers=header,
        params=param)
        if response.status_code ==401:
            print('Unauthorized; Check API Key')
            exit()
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

# Checks to see if the user has a project matching their course names, if there
# is not a new project will be created
def create_todoist_projects():
    for course_id in course_ids:
        if courses_id_name_dict[course_id] not in todoist_project_dict:
            project = todoist_api.projects.add(courses_id_name_dict[course_id])
            todoist_api.commit();
            todoist_api.sync()
            todoist_project_dict[project['name']] = project['id']
        else:
            print("Project " + courses_id_name_dict[course_id] + " exists")

# Transfers over assignments from canvas over to Todoist, the method Checks
# to make sure the assignment has not already been transferred to prevent overlap
def transfer_assignments_to_todoist():
    for assignment in assignments:
        course_name = courses_id_name_dict[assignment['course_id']]
        project_id = todoist_project_dict[course_name]

        is_added = False
        is_synced = True
        item = None

        for task in todoist_tasks:
            if config['sync_null_assignments'] == False:
                if assignment['submission_types'][0] == 'not_graded' or assignment['submission_types'][0] == 'none':
                    print("Ignoring ungraded/non-submittable assignment: " + course_name + ": " + assignment['name'])
                    is_added = True
                    break
            if assignment['unlock_at'] != None and config['sync_locked_assignments'] == False and assignment['unlock_at'] > (datetime.datetime.now() + datetime.timedelta(days=1)).isoformat():
                print("Ignoring assignment that is not yet unlocked: " + course_name + ": " + assignment['name'] + ": " + assignment['lock_explanation'])
                is_added = True
                break
            if assignment['locked_for_user'] == True and assignment['unlock_at'] == None and config['sync_locked_assignments'] == False:
                print("Ignoring assignment that is locked: " + course_name + ": " + assignment['name'] + ": " + assignment['lock_explanation'])
                is_added = True
                break
            if assignment['due_at'] == None and config['sync_no_due_date_assignments'] == False:
                print("Ignoring assignment with no due date: " + course_name + ": " + assignment['name'])
                is_added = True
                break
            if task['content'] == ('[' + assignment['name'] + '](' + assignment['html_url'] + ')' + ' Due') and \
            task['project_id'] == project_id:
                print("Assignment already synced: " + course_name + ": " + assignment['name'])
                is_added = True
                if (task['due'] and task['due']['date'] != assignment['due_at']):
                    is_synced = False
                    item = task
                    break

        if not is_added:
            if assignment['submission']['submitted_at'] == None or assignment['submission']['workflow_state'] == "unsubmitted" or assignment['submission']['attempt'] == None:
                    print("Adding assignment " + course_name + ": " + assignment['name'])
                    add_new_task(assignment, project_id)
            else:
                print("assignment already submitted " + course_name + ": " + assignment['name'])
        elif not is_synced:
            print("Updating assignment due date: " + course_name + ": " + assignment['name'] + " to " + str(assignment['due_at']))
            update_task(assignment, item)
            
    todoist_api.commit()

# Adds a new task from a Canvas assignment object to Todoist under the
# project corresponding to project_id
def add_new_task(assignment, project_id):
    todoist_api.add_item('[' + assignment['name'] + '](' + assignment['html_url'] + ')' + ' Due',
            project_id=project_id,
            date_string=assignment['due_at'],
            priority=config['todoist_task_priority'],
            labels=config['todoist_task_label_id']
            )
            
def update_task(assignment, item):
    item.update(due={
        'date': assignment['due_at']
    })

if __name__ == "__main__":
    main()
