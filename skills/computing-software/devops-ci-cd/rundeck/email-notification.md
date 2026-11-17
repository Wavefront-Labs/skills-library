---
id: computing-software.devops-ci-cd.rundeck.email-notification
name: email-notification
category: computing-software
field: devops-ci-cd
product: rundeck
tags: [rundeck, email-notification, include-log-output, job-user-email, custom-template]
level: intro
status: docs-checked
description: "Configure the built-in Rundeck email job notification: recipients, user variables, and whether the execution log is attached or inline."
sources:
  - https://raw.githubusercontent.com/rundeck/docs/4.0.x/docs/manual/notifications/email.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The built-in Email notification plugin sends an email when a job succeeds or fails.

Fields:
- **Send Email to**: comma-separated addresses. (The same field accepts comma-separated URLs for webhook notification.) Property references work: `${job.user.name}` is the user who ran the job; `${job.user.email}` is that user's email, if set in their profile.
- **Include log output**: choose one.
  - Attached as file: the file extension is controlled by template settings (see Custom Attached Log Output File in the Email Settings admin page).
  - Inline: the log goes into the body. With custom templates you must add `${logoutput.data}` to the template or the log will not appear.

For server mail configuration and custom templates, see the Email Settings administration page.

Gotcha: `${job.user.email}` only works if the executing user has an email set in their profile, so also list a fixed address.

Verify by running a job that fails and checking the inbox.

## Checked

2026-11-04. Confirmed against the Rundeck docs page Email: the Email plugin sends on success or failure, Send Email to accepts comma-separated addresses (or URLs for webhooks), the job.user.name and job.user.email references, attached vs inline log output and the logoutput.data template variable. Removed the unconfirmed Notifications tab instruction and the prerequisite claim (replaced by a pointer to the Email Settings page).

Method: documentation only; no commands were run.
