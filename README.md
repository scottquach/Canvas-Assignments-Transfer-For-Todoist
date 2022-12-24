# Canvas-Transfer-For-Todoist

not created by, affiliated with, or supported by Doist

Transferring assignments from your student Canvas account to your Todoist account couldn't be easier.

This project provides you with an easy way to transfer all of your assignments from a Canvas account into a Todoist account with appropraite due dates and assignment to auto-generated projects that match course names.

## How-To

### Easy Run

Easy run allows all configuration to be done inside of the program, avoiding the hassle of editing the api_keys file directly. Just install the dependencies and follow the instructions on screen.
- Install required packages with `pip install -r requirements.txt`
- Run `python easy_run.py` and follow up the settings

## Known Limitations

Due Date Updates: The script will update due dates when they are modified. However it will not remove a due date if one is already set in Todoist, even if it is removed in Canvas (because Todoist API does not accept "NULL" as a due date update value - so due dates will not be updated in the event that they are REMOVED in Canvas, only updated if they are added or are changed to a different date.

Name or Assignment Changes: The script will not modify or remove Todist tasks retroactively, so if a teacher deletes or modifies an assignment, it will not be removed from Todoist. In the case of a name change, a new task would be created in Todoist with the new assignment name. Note that

**Every teacher uses Canvas differently. My scripts have several hacks to handle weird things my different teachers would do (such as creating ungraded/unsubmittable assignments, locked assignments, etc)

## FAQ
Q: Why are Priority numbers different?

A: The Todoist API Priority numbers go from 1 (Default) to 4 (Very Urgent), which is the opposite as the UI (https://developer.todoist.com/rest/v2/#create-a-new-task)

Q: What are null/unsubmittable assignments?

A: Teachers can set submission method for an assignment to "none" or "not graded". This filters out those assignments.

Q: What are locked assignments?

A: Teachers can lock assignments so they cannot be viewed or done. These locks can be because a module is not unlocked, or they can be set to unlock at a certain date. If the setting to not sync locked assignments is enabled, any assignment which is locked (or is not set to unlock within the next 24 hours) will not be synced.

## Contributing
I use this regularly for my classes to sync to Todoist (which is my work System of Record), please open an issue for any problems you encounter or questions you have!

## Contributors
Thanks to all the below for their contributions!
