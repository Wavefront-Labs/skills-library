---
id: computing-software.devops-ci-cd.forgejo.soft-quota-configuration
name: soft-quota-configuration
category: computing-software
field: devops-ci-cd
product: forgejo
tags: [soft-quota, quota-default, quota-api, quota-subjects]
level: advanced
status: docs-checked
description: "Enable the experimental soft quota and set a global limit or API-managed quota groups."
sources:
  - https://forgejo.org/docs/latest/admin/advanced/quota/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Forgejo has early, still developing support for a soft quota that protects a server from high disk usage due to abuse or errors. It is soft because quota is checked only before an action starts; a started action can finish, so a push that began before the limit was reached may exceed it. Once exceeded, new operations that would increase usage are refused. Web operations denied later are not yet handled optimally in the UI.

It is off by default. Enable it with `[quota]` `ENABLED = true`.

Simple case: set a global limit for all data with `[quota.default]` `TOTAL = 2G`. The default is `-1` (unlimited) and values take unit suffixes such as 500M or 10G.

Advanced case: use the API with an admin application token. Browse `/api/swagger` for the endpoints and read the config cheat sheet for the available quota subjects. A quota group contains named rules, each with a numeric `limit` (the example uses values such as `200000000`, and `-1` for unlimited; the page does not name the unit) and `subjects` such as `size:repos:all`, `size:git:lfs` or `size:assets:all`. The page's example group restricts Git repo space tightly, gives LFS more room, allows unlimited packages and attachments, but restricts Actions artifacts. Create a group with `POST /admin/quota/groups` and assign a user with `PUT /admin/quota/groups/<GROUPNAME>/users/<USERNAME>` (under `/api/v1`).

Keep the admin API token out of shell history (the page's helper script says to delete it after setting up or ensure it is not preserved).

## Checked

Date: 2026-11-07
Confirmed against the "Soft-Quota" page, read in full including its code blocks: the soft-quota semantics and UI limitation, `[quota]` `ENABLED = true`, `[quota.default]` `TOTAL = 2G`, the `-1` default and unit suffixes, the admin application token and `/api/swagger`, the config cheat sheet reference for quota subjects, the example quota group JSON, the group create and user assign endpoints, and the shell-history warning.
Corrected: the skill claimed `limit` is "in bytes"; the page does not state the unit, so that was removed. The example description now matches the page (including the restricted Actions artifacts). Added the two API calls the page shows. The OAuth2 group sync section was read but is not covered by this skill.
Method: documentation only; no commands were run.
