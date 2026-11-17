---
id: computing-software.rpa-and-low-code.n8n.push-and-pull-changes
name: push-and-pull-changes
category: computing-software
field: rpa-and-low-code
product: n8n
tags: [n8n, source-control, push, pull, auto-publish, data-tables, merge-conflicts]
level: advanced
status: docs-checked
description: "Push and pull n8n work with Git: who may do it, what is committed, auto publish modes, owner remapping, and how workflows, credentials and data tables merge."
sources:
  - https://docs.n8n.io/administer/use-source-control-and-environments/push-and-pull-changes
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

## Roles
Pull needs instance owner or admin. Push needs instance owner, admin or project admin.

## Pull
Select **Pull** in the main menu; **Pull and override** replaces local work with Git. New variable or credential stubs must be populated before use. Deleted-in-Git resources are not removed automatically; n8n asks whether to delete outdated ones. Pulling a published workflow unpublishes then republishes it (seconds of downtime).
- Owner: matching email keeps the owner, else the puller owns it. Projects match by ID; if missing n8n creates it and the puller becomes its project admin.
- **Auto publish** in the pull modal: **Off** (default), **If workflow already published**, **On**. Archived workflows are never published. Failures (validation errors, missing credentials) show in a results modal. API pull parameter `autoPublish`: `none`, `published`, `all`.

## Push commits
Workflows (with tags and owner email; you choose which), credential stubs (ID, name, type; other fields only if expressions), variable stubs (ID and name), data table schemas (not rows), projects, folders.

## Merge behaviour
- Workflows: Git is the source of truth; no conflict detection. Push overwrites Git, pull overwrites local. Push right after finishing edits, move work in one direction (develop, push, pull to production) and push only needed workflows.
- Credentials, variables, tags: pull creates missing ones, does not update existing unless a variable value was set via API, the credential name changed (Git wins) or a tag was renamed. Push overwrites the entire variables and tags files.
- Data tables: matched by name within a project; pull adds new columns and removes missing ones (that column's data is lost; warning shown). A local table absent from Git is deleted with its rows on pull; forced pulls (API, automation) skip the confirmation, so push first to keep it.

For different credentials per environment use external secrets.

## Checked
Method: docs-checked 2026-11-09 against the n8n "Push and pull changes" page (docs.n8n.io, read in full).
Nothing removed; roles, auto publish modes, what is committed and the merge rules all match the page.
