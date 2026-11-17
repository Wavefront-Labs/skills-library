---
id: computing-software.web-development.appwrite.appwrite-database-backups-policies
name: appwrite-database-backups-policies
category: computing-software
field: web-development
product: appwrite
tags: [appwrite, databases, backups, restore, cloud]
level: practitioner
status: docs-checked
description: "Schedule backup policies, take manual backups and restore into a new database on Appwrite Cloud."
sources:
  - https://github.com/appwrite/website/blob/main/src/routes/docs/products/databases/backups/+page.markdoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: protect database data on Appwrite Cloud.

Availability: backups are available on Appwrite Cloud for Pro, Scale and Enterprise customers. All backups are encrypted, remotely stored hot backups, so there is zero downtime.

Policies (automated backups at scheduled intervals):
1. In the Console sidebar click Databases, select your database, open the Backups tab.
2. Click Create Policies and pick a pre-defined policy. On Pro you get a Daily policy; Scale and Enterprise get more pre-defined policies and custom ones where you set how often backups run, how long they are retained and when they run.
3. Click Create.

Manual backup: Backups tab > Manual Backup (the page also calls it Create Manual). Time depends on database size; progress shows in a floating status bar at the bottom of the screen.

Restore: you need an existing backup. Backups tab > options menu on the backup > Restore, enter the new database name and an optional database ID, then click Restore. Progress shows in a floating bar across the project.

Best practices in the docs: add multiple policies based on how often the database changes; use custom policies with longer retention for critical data; tune frequency and retention to data sensitivity.

Gotcha: the restore dialog asks for a new database name and optional ID, so check which database your app points at after restoring.

## Checked

2026-11-04. Confirmed against the Appwrite docs page Backups (databases/backups): plan availability, encryption, remote storage, hot backups, policy creation steps, Pro Daily policy, Scale and Enterprise custom policies, manual backup, restore inputs and status bars, and best practices. Removed: the claim that self-hosted users back up manually and that a restore never overwrites the old database, because the page states neither.
Method: documentation only; no commands were run.
