---
id: computing-software.cloud-infrastructure-engineering.saltstack.jobs-saltutil-management
name: jobs-saltutil-management
category: computing-software
field: cloud-infrastructure-engineering
product: saltstack
tags: [saltstack, jobs, saltutil, find-job, kill-job, term-job, proc]
level: practitioner
status: docs-checked
description: "Inspect and stop running Salt jobs on a minion with the proc directory and saltutil.running, find_job, signal_job, term_job and kill_job."
sources:
  - https://raw.githubusercontent.com/saltstack/salt/master/doc/topics/jobs/index.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Managing running jobs with saltutil

Each minion keeps a proc directory under the cachedir (default `/var/cache/salt/{master|minion}/proc`) with one file per running job, named by its jid.

saltutil functions:
- `running`: data for all running jobs in the proc directory.
- `find_job <jid>`: details of one job.
- `signal_job`: send a signal to the job.
- `term_job <jid>`: SIGTERM (15) to its process.
- `kill_job <jid>`: SIGKILL (9) to its process.

These are called as `saltutil.<function>` against a minion.

## Checked

2026-11-09. Read in full the Salt Job Management page (doc/topics/jobs/index.rst, master branch): Minion proc System and Functions in the saltutil Module. Nothing removed.

Method: documentation only; no commands were run.
