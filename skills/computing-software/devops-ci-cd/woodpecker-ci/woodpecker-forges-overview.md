---
id: computing-software.devops-ci-cd.woodpecker-ci.woodpecker-forges-overview
name: woodpecker-forges-overview
category: computing-software
field: devops-ci-cd
product: woodpecker-ci
tags: [forges, multi-forge, forge-support]
level: practitioner
status: docs-checked
description: "Compare Woodpecker forge support and understand the experimental multi-forge limits."
sources: ["https://woodpecker-ci.org/docs/administration/configuration/forges/overview"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Woodpecker forges overview

Supported forges: GitHub, Gitea, Forgejo, GitLab, Bitbucket and Bitbucket Datacenter. All support push, tag and pull-request events, multiple workflows and the `when.path` filter. Release events are not supported on Bitbucket or Bitbucket Datacenter. Deploy events through webhooks work on GitHub only, though a deployment can be triggered from Woodpecker for any forge. Pull-request-metadata events are unsupported on Bitbucket and Bitbucket Datacenter.

For other forges, addon forges are available.

Multiple forges are experimental; do not use them in public or untrusted environments. Only one forge can be configured with environment variables. Additional forges are added by an admin under `Settings -> Forges` and live in the database. The environment forge is written back on every server start.

Admin: `WOODPECKER_ADMIN` is matched by login name only, so a user with a matching login on any connected forge becomes admin.

Login restrictions: `WOODPECKER_ORGS` applies to all forges, but organization names are unique only per forge, so someone could create a same-named organization on another forge. With multiple forges leave `WOODPECKER_ORGS` empty and set `Allowed organizations` per forge under `Advanced options`. Matching is case-insensitive and only at login. For GitLab use the group `full_path`.

Known limitation: users are stored per forge, so one person logging in through two forges gets two accounts.

## Checked

2026-11-03. Read the Woodpecker forges overview page and confirmed the supported forge list, event support matrix, addon forges, experimental multiple-forge limits, per-forge allowed organizations, case-insensitive matching at login and per-forge accounts. Removed: the WOODPECKER_ADMIN_PRIMARY_FORGE_ONLY setting, which the page does not document. 

Method: documentation only; no commands were run.
