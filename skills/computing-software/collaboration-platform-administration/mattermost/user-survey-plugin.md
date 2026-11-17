---
id: computing-software.collaboration-platform-administration.mattermost.user-survey-plugin
name: user-survey-plugin
category: computing-software
field: collaboration-platform-administration
product: mattermost
tags: [user-survey, nps, survey-plugin, export-responses]
level: practitioner
status: docs-checked
description: "Run self-hosted Mattermost User Survey: enable the plugin, schedule a survey with expiry and team scope, required NPS question and CSV export."
sources: ["https://docs.mattermost.com/administration-guide/configure/manage-user-surveys.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Managing user surveys

The Mattermost User Survey integration lets self-hosted admins gather direct feedback. Responses stay inside your deployment and no telemetry goes back to Mattermost. It is the recommended approach for new deployments, replacing the deprecated User Satisfaction Survey plugin. Only system admins can enable it, create surveys and export responses. It needs Mattermost v9.11.2 or later and is pre-packaged from v9.11.2 (ESR) and Cloud v10; older releases need the plugin binary from its releases page uploaded. Update it as new versions appear; updates are generally seamless.

Enable under System Console > Plugins > User Survey, then configure under Survey setup:
1. Send next survey at: date and time the rollout starts. Only one survey can be active at a time, so schedule after the current one expires or end the active one.
2. Survey expiry (days): how long it accepts responses.
3. Team targeting: all users, all users on chosen teams, or exclude teams.
4. Survey message text: the intro users see.
5. Linear scale question (1 to 10): required, used to calculate the NPS score.
6. Textual question: required feedback question.
7. A further optional textual question.
8. Save. The survey shows under Active and past surveys once shared.

When the survey starts, every user receives a direct message from a feedback bot. They must answer the required questions to submit. Select Export responses to download a CSV of NPS scores and responses; exporting during an active survey returns what has been collected so far.

## Checked

Confirmed against the Manage user surveys page: sysadmin-only setup, v9.11.2 compatibility and pre-packaging, enable path, the eight survey setup fields, one active survey at a time, the feedback bot message and CSV export. Nothing removed.

Method: docs-checked 2026-11-09 against the full administration-guide/configure/manage-user-surveys page (source rst from the mattermost/docs repo).
