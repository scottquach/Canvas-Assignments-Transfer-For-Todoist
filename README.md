# Canvas-Assignments-Transfer-For-Todoist
not created by, affiliated with, or supported by Doist

Transferring assignments from your student Canvas account to your Todoist account couldn't be easier.

This project provides you with an easy way to transfer all of your assignments from a Canvas account into a Todoist account with appropraite due dates and assignment to auto-generated projects that match course names.

## How-To

### Easy Run
Easy run allows all configuration to be done inside of the program, avoiding the hassle of editing the api_keys file directly. Just install the dependencies and follow the instructions on screen.
- Install required packages with `pip install -r requirements.txt`
- Run `python easy_run.py`

##Known Limitations
**With the exception of due date, the script will not update or change a task that already exists in Todoist. So, if a teacher deletes or modifies an assignment, it will not retroactively remove from Todoist. In the case of a name change, a new task would be created in Todoist with the new assignment name.

**Every teacher uses Canvas differently. My scripts have several hacks to handle weird things my different teachers would do (such as creating ungraded/unsubmittable assignments, locked assignments, etc)

## Contributing
I use this regularly for my classes to sync to Todoist (which is my work System of Record), happy to discuss any features or requests
