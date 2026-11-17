---
id: computing-software.devops-ci-cd.rundeck.project-calendars
name: project-calendars
category: computing-software
field: devops-ci-cd
product: rundeck
tags: [rundeck, project-calendars, job-schedule, add-calendar, calendar-jobs]
level: practitioner
status: docs-checked
description: "Add a calendar at project level in Rundeck and apply it to selected jobs or all jobs in the project to affect their schedules."
sources:
  - https://raw.githubusercontent.com/rundeck/docs/4.0.x/docs/manual/calendars/project-calendars.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Project calendars have the same form as system calendars; the difference is that they apply to jobs in one project.

Steps:
1. Open the new Calendars menu in the project sidebar.
2. Click **Add Calendar** and fill the form as for a system calendar.
3. In the **Jobs** section choose where it applies. By default it is assigned to no jobs.
4. Click "Add a Job..." and click a job name to add it. Use "Remove" to drop one.
5. Or tick "Apply this Calendar to All Jobs" to cover the whole project.
6. Save the calendar.

Verify: the Jobs page now lists the calendars applied to each job's schedule.

Gotcha: by default the calendar is assigned to no jobs, so select jobs or tick the all-jobs box.

## Checked

2026-11-04: the project sidebar menu, the form matching system calendars, the Jobs section default, Add a Job and Remove, the all-jobs checkbox and the Jobs page listing confirmed against the Rundeck Project Calendars page.

Method: documentation only; no commands were run.
