---
id: computing-software.devops-ci-cd.rundeck.project-schedules
name: project-schedules
category: computing-software
field: devops-ci-cd
product: rundeck
tags: [rundeck, project-schedules, retain-schedules, crontab-schedule, schedule-yaml]
level: advanced
status: docs-checked
description: "Define reusable project schedules in Rundeck Enterprise, assign them to jobs with option overrides, and manage them as YAML."
sources:
  - https://raw.githubusercontent.com/rundeck/docs/4.0.x/docs/manual/schedules/project-schedules.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Project Schedules (Enterprise) define schedules independently of jobs and can apply to any job in the project. Currently only project admins can access the module.

Create: project sidebar **Schedules**, **New Schedule**, enter Name (required) and optional Description, choose *Simple* or *Crontab*, optionally a Time Zone, Save.

Assign: Actions, **Assign To Job**, click jobs to assign, **Unassign** to remove. **Set Job Options...** takes `-optname value` pairs used when this schedule fires instead of the job defaults.

Retain Schedules (from 5.2.0): tick it so importing a job without schedules (for example via SCM) keeps its schedule association. Default off, for backwards compatibility. It does not affect schedules set directly on the job.

Other actions: Download Schedule (YAML), Upload Schedule, Delete, Bulk Delete.

YAML definition (several per file):

```yaml
- description: every 5 minutes
  name: Test
  project: schedules-demo
  timeZone: ''
  type: CRON
  crontabString: 0 */5 * ? * * *
```

`type: SIMPLE` instead uses a `schedule` map of `hour`, `minute`, `dayOfWeek` (`*` or `SUN,MON,...`) and `month` (`*` or `JAN,FEB,...`). Crontab uses Quartz format.

Disable the feature with `rundeck.feature.projectSchedules.enabled=false` in rundeck-config.properties.

## Checked

2026-11-04: admin-only access, the create and assign steps, job option overrides, Retain Schedules, the other actions, the YAML definition fields and the feature flag confirmed against the Rundeck Project Schedules page.

Method: documentation only; no commands were run.
