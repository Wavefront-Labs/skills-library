---
id: computing-software.data-engineering.metabase.transform-jobs-and-runs
name: transform-jobs-and-runs
category: computing-software
field: data-engineering
product: metabase
tags: [transform-jobs, transform-tags, runs, cron, failure-emails, dependencies]
level: advanced
status: docs-checked
description: "Schedule Metabase transforms with jobs and tags: default tags, dependency execution rules, disabling and deleting jobs, the Runs page and failure email routing."
sources:
  - https://www.metabase.com/docs/latest/data-modeling/transforms/jobs-and-runs
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Scheduling: jobs run transforms based on transform tags. Schedules can be built-in or custom cron expressions, evaluated in the Metabase system timezone. A job runs every transform that carries any of its tags. Default tags are hourly, daily, weekly and monthly; you can rename, delete or add tags.

Dependencies:
- Jobs also run upstream dependencies that are not up to date, even untagged ones, and run them first.
- A tagged dependency is skipped if none of its own job schedules have come due since it last succeeded.
- An untagged dependency is skipped once it has succeeded at least once.

Disable and delete: disabling a job keeps its tags and schedule. Disable All does not stop newly created jobs starting enabled. Deleted jobs cannot be restored, and deleting a job does not delete its transforms.

Runs: the Runs page lists manual and scheduled runs with times in the server timezone. The Tags column shows only the transform's own tags, which may not explain why a run happened, since a dependency can trigger it.

Failure emails (need email set up): scheduled failures email the last editor, the creator, or admins if neither is active, one email per job run. Admins also get a daily digest of failed or timed-out scheduled runs; manual runs are excluded and nothing is sent if nothing failed.

## Checked

Method: 2026-11-08 read the cited page in full as raw markdown from the Metabase docs repository. Every claim matched the page; no content changes.
