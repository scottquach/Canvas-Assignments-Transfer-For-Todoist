# Canvas-Assignments-Transfer-For-Todoist
not created by, affiliated with, or supported by Doist

Easily transfers assignments from your student Canvas account to your Todoist account.

This project provides you with an easy way to transfer all of your assignments from a Canvas account into a Todoist account with appropriate due dates and assignment to auto-generated projects that match course names.

## How-To

### Prerequisites:
 **You will first need an API key for both Canvas and Todoist**
- On Canvas website Click on "Account", then "settings". Click on ```New Access Token``` under Approved Integrations
- On Todoist desktop or website go to settings, then Integrations. The API token is listed at the bottom of the ```Integrations Tab```

### Easy Run
Easy run allows all configuration to be done inside of the program, avoiding the hassle of editing the config.json file directly. Just install the dependencies and follow the instructions on screen.
- Install required packages with `pip install -r requirements.txt`
- Run `python easy_run.py`
- Follow the configuration prompts to paste in your API Keys and provide any custom or advanced configuration details.

### Manual Setup
If you don't want to use easy run for whatever reason, you can edit the `config.json` file directly, just follow the steps below.
1) Replace the "Todoist_api_Key" value with your todoist API key
2) Replace the "Ccanvas_api_key" value with your Canvas API Key
3) Replace the "canvas_api_heading" value with your Canvas URL (defualt is https://canvas.instructure.com)
4) replace the "todoist_task_priority" with the priority value you would like the tasks created at (note that API values are opposite of GUI values - i.e. "1" equals a Priority 4, and "4" equals a Priority 1)
5) If desired, place the label IDs of any Todoist task labels you would like added in the "Todoist_task_labels" field.
6) Set the "Configured" value to "yes"

**You will then need the course ID of the classes whose assignments you would like to transfer. This is easy to find thanks to an included script titled ```retrieve_canvas_course_ids```**
- Run the script by calling ```python retrieve_canvas_course_ids.py```
- Your courses will be listed with the associated ID
- This step is necessary and not automated **because some teachers don't archive their classes for the next quarter and old assignments could be added by mistake**

**Install dependencies**
- Install dependencies with `pip install -r requirements.txt`

**Run the main script**
- Run the main script by calling ```python canvas_to_todoist.py```
- The script will run and transfer assignments over to Todoist
  - Assignments will be checked for overlap, so running the script multiple times won't re-add assignments that already exist in Todoist.
- Assignments will be added to automatically generated projects in Todoist. The project names will match with the official course names pulled from Canvas

## Bugs/Questions

Q: How do I re-run the initial config setup?
A: Simply set "configured" to false (or alternatively, delete the config.json and replace with a new downloaded one.

Q: I'm getting some keyErrors 
A: This most likely is due to a change in your canvas classes that no longer match the JSON. Select "no" and then re-select the class IDs.

## Known Limitations/Current Issues (as of Jan 2022)
- Tasks are only synced initially by name; thereafter any modifications made in Canvas will not sync if the task by the same name already exist. For example, if the Due Date is updated in Canvas, the script won't update it in Todoist unless you delete/complete/remove the Todoist task.
- Some teachers may enter pages or content in as an assignment as canvas (that can't be completed or submitted). Since those can't be differentiated from via API, they will sync as tasks on each Sync. 

## Contributing
I'm still active in the community so feel free to submit an issue or PR for anything that comes up and I'm happy to help!
