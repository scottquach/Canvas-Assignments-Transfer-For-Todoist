# Canvas-Transfer-For-Todoist
<!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->
[![All Contributors](https://img.shields.io/badge/all_contributors-2-orange.svg?style=flat-square)](#contributors-)
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
- Run `python easy_run.py` and follow up the settings

## Known Issues/Limitations

Due Date Updates: The script will update due dates when they are modified. However it will not remove a due date if one is already set in Todoist, even if it is removed in Canvas, as Todoist API does not accept "NULL" as a due date update value.  Due dates will not be updated in the event that they are REMOVED in Canvas, only updated if they are added or are changed to a different date.

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
    </tr>
  </tbody>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->