# Canvas-Transfer-For-Todoist
<!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->
[![All Contributors](https://img.shields.io/badge/all_contributors-6-orange.svg?style=flat-square)](#contributors-)
<!-- ALL-CONTRIBUTORS-BADGE:END -->

not created by, affiliated with, or supported by Doist

Transferring assignments from your student Canvas account to your Todoist account couldn't be easier.

This project provides you with an easy way to transfer all of your assignments from a Canvas account into a Todoist account with appropraite due dates and assignment to auto-generated projects that match course names.

## How-To

### Easy Run

Easy run allows all configuration to be done inside of the program, avoiding the hassle of creating the config file directly.
Just install the dependencies and follow the instructions on screen.

- Obtain your API Keys for Todoist and Canvas
- On Canvas desktop go to settings and click on ```New Access Token``` under Approved Integrations
- On Todoist desktop go to settings and the API token will be listed under the ```Integrations Tab```. You can also generate an application-specific token at https://developer.todoist.com/appconsole.html
- Install required packages with `pip install -r requirements.txt`
- Run `python easy_run.py` and follow up the prompts
- A config.json file will be created with your selections so it can be run again in the future using the same keys and/or classes

## Known Issues/Limitations

> :exclamation: Every teacher uses Canvas slightly differently. We cannot be 100% responsible for any grades or assignments missed. It is YOUR resoponsibility to reeview Canvas regularly to ensure you are not behind.

Due Date Updates: The script will update due dates on tasks when the following conditions are met:
1) The assignment in Canvas DOES have a due date
2) The task in Todoist either does NOT have a due date, OR it has a due date that is LATER (in the future from) the Canvas Due Date..

It will not REMOVE adue dates from Todoist (even if they are removed in Canvas), so you can set an artifical 'due date' in Todoist for assignments with no due date.
It will also not update due dates if the due date is set earier than the one in Canvas (allowing you to artifically 'move' due dates earlier, but not later)

Name or Assignment Changes: The script will not modify or remove Todist tasks retroactively, so if a teacher deletes or modifies an assignment, it will not be removed from Todoist. In the case of a name change, a new task would be created in Todoist with the new assignment name.

Graded Assignments: This script ignores any assignments once they are graded.

> :warning: This means that if a teacher enters "0" the assignment will be ignored, even if you have additional opportunities to submit it. Thus, it is recommended that you do not remove a task from Todoist until you are complete.

Submissions: This script assumes assignments with submissions do not need to be added.

> :zap: You must keep track of any re-submissions or regrades seperately; this script does not have logic to handle them.

Duplicate tasks: Tasks are tracked based on the the class name and assigment title within Canvas. The script does not delete or remove tasks. If a teacher renames an assignment, you will end up with two assignments in Todoist (one under the old name, one under the new name) - only the new one will be kept up to date with any date changes.

:point_up: Every teacher uses Canvas differently - there are several options available to handle different things teachers do in Canvas (such as creating ungraded/unsubmittable assignments, locked assignments, etc).

I recommend synching all assignments at the beginning of the semester, then adjusting your settings to exclude ungraded and null assignments once they are fully added.

## FAQ
Q: Why are Priority numbers different?

A: The Todoist API Priority numbers go from 1 (Default) to 4 (Very Urgent), which is the opposite as the UI (https://developer.todoist.com/rest/v2/#create-a-new-task)

Q: What are null/unsubmittable assignments?

A: Teachers can set submission method for an assignment to "none" or "not graded". This filters out those assignments (since you can't actually submit them)

Q: What are locked assignments?

A: Teachers can lock assignments so they cannot be viewed or done. These locks can be because a module is not unlocked, or they can be set to unlock at a certain date. If the setting to not sync locked assignments is enabled, any assignment which is locked (or is not set to unlock within the next 24 hours) will not be synced.

## Contributing
I use this regularly for my classes to sync to Todoist (which is my work System of Record), please open an issue for any problems you encounter or questions you have!

## Troubleshooting
If you encounter any issues, please open an Issue with the appropriate data

## Contributors
Thanks to all the below for their contributions!

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tbody>
    <tr>
      <td align="center"><a href="https://scottquach.com/"><img src="https://avatars.githubusercontent.com/u/11187380?v=4?s=100" width="100px;" alt="Scott Quach"/><br /><sub><b>Scott Quach</b></sub></a><br /><a href="https://github.com/stacksjb/Canvas-Assignments-Transfer-For-Todoist-S/commits?author=scottquach" title="Code">💻</a></td>
      <td align="center"><a href="https://github.com/stacksjb"><img src="https://avatars.githubusercontent.com/u/2865491?v=4?s=100" width="100px;" alt="Jesse"/><br /><sub><b>Jesse</b></sub></a><br /><a href="https://github.com/stacksjb/Canvas-Assignments-Transfer-For-Todoist-S/commits?author=stacksjb" title="Code">💻</a> <a href="https://github.com/stacksjb/Canvas-Assignments-Transfer-For-Todoist-S/issues?q=author%3Astacksjb" title="Bug reports">🐛</a></td>
      <td align="center"><a href="http://www.andreicozma.com"><img src="https://avatars.githubusercontent.com/u/14914491?v=4?s=100" width="100px;" alt="Andrei Cozma"/><br /><sub><b>Andrei Cozma</b></sub></a><br /><a href="https://github.com/stacksjb/Canvas-Assignments-Transfer-For-Todoist-S/issues?q=author%3Aandreicozma1" title="Bug reports">🐛</a></td>
      <td align="center"><a href="http://linkedin.com/in/nassuelvc"><img src="https://avatars.githubusercontent.com/u/34118212?v=4?s=100" width="100px;" alt="Nassuel N. Valera"/><br /><sub><b>Nassuel N. Valera</b></sub></a><br /><a href="https://github.com/stacksjb/Canvas-Assignments-Transfer-For-Todoist-S/issues?q=author%3ANassuel" title="Bug reports">🐛</a></td>
      <td align="center"><a href="http://stemplayeronline.com"><img src="https://avatars.githubusercontent.com/u/47042841?v=4?s=100" width="100px;" alt="Luke Weiler"/><br /><sub><b>Luke Weiler</b></sub></a><br /><a href="https://github.com/stacksjb/Canvas-Assignments-Transfer-For-Todoist-S/issues?q=author%3Alukew3" title="Bug reports">🐛</a></td>
      <td align="center"><a href="http://web.cs.ucdavis.edu/~cdstanford"><img src="https://avatars.githubusercontent.com/u/9029697?v=4?s=100" width="100px;" alt="Caleb Stanford"/><br /><sub><b>Caleb Stanford</b></sub></a><br /><a href="#ideas-cdstanford" title="Ideas, Planning, & Feedback">🤔</a> <a href="#mentoring-cdstanford" title="Mentoring">🧑‍🏫</a></td>
    </tr>
  </tbody>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->
