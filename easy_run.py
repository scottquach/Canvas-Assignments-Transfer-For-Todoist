import requests
import re
import json
from todoist.api import TodoistAPI
from requests.auth import HTTPDigestAuth

keys = []
canvas_api_heading = 'https://canvas.instructure.com'
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
    select_courses(keys)
    print("Working...")
    load_todoist_projects()
    load_assignments()
    load_todoist_tasks()
    create_todoist_projects()
    transfer_assignments_to_todoist()
    print("Done!")

# Makes sure that the user has their api keys set up and sets api variables
def initialize_api():
    with open("api_keys.txt") as api_file:
        keys = api_file.readlines()
    # print(keys);

    if len(keys) == 0 :
        print("Your Todoist API key has not been configured. To add an API token, go to your Todoist settings and copy the API token listed under the Integrations Tab. Copy the token and paste below when you are done.")
        keys.append(input(">") + "\n");
        f = open("api_keys.txt", "w")
        f.writelines(keys)
        f.close()
        print("Your Canvas API key has not been configured. To add an API token, go to your Canvas settings and click on New Access Token under Approved Integrations. Copy the token and paste below when you are done.")
        keys.append(input(">") + "\n")
        f = open("api_keys.txt", "w")
        f.writelines(keys)
        f.close()
    else:
        if keys[0] == "Replace THIS line with the Todoist API token. Remove trailing spaces\n" :
                print("Your Todoist API key has not been configured. To add an API token, go to your Todoist settings and copy the API token listed under the Integrations Tab. Copy the token and paste below when you are done.")
                keys[0] = input(">") + "\n"
                f = open("api_keys.txt", "w")
                f.writelines(keys)
                f.close()
        if keys[1] == "Replace THIS line with the Canvas API token. Remove Trailing spaces\n":
            print("Your Canvas API key has not been configured. To add an API token, go to your Canvas settings and click on New Access Token under Approved Integrations. Copy the token and paste below when you are done.")
            keys[1] = input(">") + "\n"
            f = open("api_keys.txt", "w")
            f.writelines(keys)
            f.close()

    #create todoist_api object globally
    global todoist_api
    todoist_api = TodoistAPI(keys[0].strip())
    todoist_api.reset_state()
    todoist_api.sync()
    header.update({"Authorization":"Bearer " + keys[1].strip()})

# Allows the user to select the courses that they want to transfer while generating a dictionary
# that has course ids as the keys and their names as the values
def select_courses(keys):
    response = requests.get(canvas_api_heading + '/api/v1/courses',
            headers=header, params=param)
    with open("api_keys.txt") as api_file:
        keys = api_file.readlines()
    if keys[2].strip() != "Replace THIS line and lines AFTER with the course ID of the course you want assignments to trasfer. Remove trailing spaces": #or keys[2:]
        use_previous_input = input("You have previously selected courses. Would you like to use the courses selected last time? (y/n) ")
        print("")
        if use_previous_input == "y" or use_previous_input == "Y":
            for course_id in keys[2:]:
                course_ids.append(int(course_id.strip()))
            for course in response.json():
                courses_id_name_dict[course.get('id', None)] = re.sub(r'[^-a-zA-Z._\s]', '', course.get('name', ''))
            return

    # If the user does not choose to use courses selected last time
    i = 1
    for course in response.json():
        courses_id_name_dict[course.get('id', None)] = re.sub(r'[^-a-zA-Z._\s]', '', course.get('name', ''))
        if course.get('name') != None:
            print(str(i) + ") " + courses_id_name_dict[course.get('id', "")]  + ': ' + str(course.get('id', "")))
        i+=1
    print("\nEnter the courses you would like to add to todoist by entering the numbers of the items you would like to select. Seperate numbers with spaces")
    my_input = input(">")
    input_array = my_input.split()
    for item in input_array:
        course_ids.append(response.json()[int(item)-1].get('id', None))

    #write course ids to api_keys.txt
    write_list = keys[0:2]
    for item in course_ids:
        write_list.append(str(item) + '\n')
    f = open("api_keys.txt", "w")
    f.writelines(write_list)
    f.close()


# Iterates over the course_ids list and loads all of the users assignments
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
            print("assignment already synced")
    todoist_api.commit()

# Adds a new task from a Canvas assignment object to Todoist under the
# project coreesponding to project_id
def add_new_task(assignment, project_id):
    todoist_api.add_item(assignment['name'] + ' Due',
            project_id=project_id,
            date_string=assignment['due_at'])

if __name__ == "__main__":
    main()
