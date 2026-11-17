---
id: computing-software.collaboration-platform-administration.mattermost.user-satisfaction-survey-plugin-deprecated
name: user-satisfaction-survey-plugin-deprecated
category: computing-software
field: collaboration-platform-administration
product: mattermost
tags: [satisfaction-survey, surveybot, deprecated-plugin, survey-schedule]
level: intro
status: docs-checked
description: "Legacy Mattermost User Satisfaction Surveys plugin: deprecated from v10.11, 21-day scheduling rules, collected data and how to disable it."
sources: ["https://docs.mattermost.com/administration-guide/manage/user-satisfaction-surveys.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# User satisfaction surveys (deprecated)

The User Satisfaction Surveys plugin is deprecated from Mattermost v10.11 and no longer pre-packaged for new deployments; existing deployments with it enabled continue, and the User Survey integration is recommended instead.

Enabled by default (before v10.11) as a pre-packaged plugin. To disable surveys and all data collection, disable the User Satisfaction Surveys plugin in System Console > Plugins > Plugin Management. If only surveys are switched off in the plugin's own configuration while the plugin stays enabled, surveys are not scheduled but users can still send written feedback. Disabled settings stay disabled across server upgrades.

Scheduling: users get a survey 21 days after each server upgrade if the plugin and surveys are enabled, the account is older than 21 days, the user has not completed or been sent a survey in the last 90 days, and the server version is newer than the last survey version excluding dot releases. At most one survey per user every 90 days. Admins get an email and a direct message from Surveybot with the scheduled date.

Receiving: all users get a Surveybot direct message on their next login or page refresh, with an optional 0 to 10 score on how likely they are to recommend Mattermost plus optional written feedback. Data is collected only when a user answers: score, feedback, timestamp, server and web app version, installation date, diagnostic ID, license ID and edition if applicable, user role, account creation time and user ID.

On a private network behind a firewall, survey data is not sent unless outbound connections are allowed for this plugin.

## Checked

2026-11-03. Confirmed against the Mattermost documentation page https://docs.mattermost.com/administration-guide/manage/user-satisfaction-surveys (deprecation note, scheduling, data collected). Nothing removed.

Method: documentation only; no commands were run.
