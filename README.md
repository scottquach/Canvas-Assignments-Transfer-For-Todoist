# Canvas-Assignments-Transfer-For-Todoist
not created by, affiliated with, or supported by Doist

Transferring assignments from your student Canvas account to your Todoist account couldn't be easier.

This project provides you with an easy way to transfer all of your assignments from a Canvas account into a Todoist account with appropraite due dates and assignment to auto-generated projects that match course names.

## How-To

### Easy Run
Easy run allows all configuration to be done inside of the program, avoiding the hassle of editing the api_keys file directly. Just install the dependencies and follow the instructions on screen.
- Install required packages with `pip install -r requirements.txt`
- OPTIONAL: If you want to assign labels to tasks, create them in Todoist, then run `python get_todoist_labels` and copy down the label IDs you would like to have assigned to the tasks
- Run `python easy_run.py` and follow up the settings

##Known Limitations
**With the exception of due date, the script will not update or change a task that already exists in Todoist. So, if a teacher deletes or modifies an assignment, it will not retroactively remove from Todoist. In the case of a name change, a new task would be created in Todoist with the new assignment name. Note that due dates will not be updated in the event that they are REMOVED in Canvas, only updated if they are added or are changed to a different date.

**Every teacher uses Canvas differently. My scripts have several hacks to handle weird things my different teachers would do (such as creating ungraded/unsubmittable assignments, locked assignments, etc)

##FAQ
Q: Why are Priority numbers different?

A: The Todoist API Priority numbers go from 1 (Default) to 4 (Very Urgent), which is the opposite as the UI (https://developer.todoist.com/rest/v1/#tasks)

Q: My Labels are not working

A: You must enter the Label ID numbers, not the Label names. Use the get_todoist_labels.py script to pull your labels and identify their ids.

Q: What are null/unsubmittable assignments?

A: Teachers can set submission method for an assignment to "none" or "not graded". This filters out those assignments.

Q: What are locked assignments?

A: Teachers can lock assignments so they cannot be viewed or done. These locks can be because a module is not unlocked, or they can be set to unlock at a certain date. If the setting to not sync locked assignments is enabled, any assignment which is locked (or is not set to unlock within the next 24 hours) will not be synced.

## Contributing
I use this regularly for my classes to sync to Todoist (which is my work System of Record), happy to discuss any features or requests
