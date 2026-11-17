---
id: computing-software.systems-network-administration.healthchecks.project-transfers-limits
name: project-transfers-limits
category: computing-software
field: systems-network-administration
product: healthchecks
tags: [healthchecks, transfer-check, transfer-project, check-limit, billing-plan-limits]
level: practitioner
status: docs-checked
description: "Move a Healthchecks check between projects, transfer project ownership by email confirmation, and understand how check limits count across owned projects."
sources:
  - https://raw.githubusercontent.com/healthchecks/healthchecks/master/templates/docs/projects_teams.md
  - https://raw.githubusercontent.com/healthchecks/healthchecks/master/templates/docs/autoprovisioning.md
  - https://raw.githubusercontent.com/healthchecks/healthchecks/master/templates/docs/api.md
  - https://raw.githubusercontent.com/healthchecks/healthchecks/master/templates/docs/self_hosted.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Transfer a check to another project: open the check's details page and click "Transfer to Another Project...". The check keeps its ping address. The dialog lists only projects where you are a Team Member or Manager.

Transfer a project to another account (owner only): on the project's Settings page click "Transfer Project...", pick a current team member as new owner and click "Initiate Transfer". The new owner must confirm by email. You then become a Team Member.

Check limits: each billing plan has a Check Limit covering the total checks across all projects you own. Reaching it blocks creating new checks. Checks in projects where you are only a member do not count.

Example from the docs: on a plan with a limit of 100, if Project A has 70 checks, Project B can hold at most 30.

Related limits: free accounts allow 20 checks (API create returns 403 at the limit); auto-provisioning can exceed the limit temporarily, up to twice the limit.

Self-hosted admins can raise per-user limits in the admin panel.

## Checked

2026-11-04. Confirmed against the Healthchecks Projects and Teams, Auto Provisioning, Management API and self-hosted pages: the check and project transfer steps and button names, the email confirmation, role change after transfer, check limit counting with the 70 and 30 example under a limit of 100, the 20-check free limit and 403, the two-times auto-provisioning headroom, and raising per-user limits in the admin panel. Nothing removed.

Method: documentation only; no commands were run.
