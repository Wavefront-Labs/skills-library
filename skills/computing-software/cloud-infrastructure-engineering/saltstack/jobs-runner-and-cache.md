---
id: computing-software.cloud-infrastructure-engineering.saltstack.jobs-runner-and-cache
name: jobs-runner-and-cache
category: computing-software
field: cloud-infrastructure-engineering
product: saltstack
tags: [saltstack, jobs, jobs-runner, lookup-jid, list-jobs, keep-jobs-seconds]
level: practitioner
status: docs-checked
description: "Find and replay Salt job results with the jobs runner (active, list_jobs, lookup_jid) and tune cached job retention with keep_jobs_seconds."
sources:
  - https://raw.githubusercontent.com/saltstack/salt/master/doc/topics/jobs/index.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Jobs runner and job cache

Run on the master:

```
salt-run jobs.active
salt-run jobs.list_jobs
salt-run jobs.lookup_jid <jid>
```

- `active`: runs `saltutil.running` on all minions and shows running jobs compactly, plus which minions have finished and which are still awaited.
- `list_jobs`: cached data for fully or partly returned jobs; use it to find a jid.
- `lookup_jid`: return data for a jid, matching what the original `salt` command displayed.

Retention: return data is cached on the master for 86400 seconds by default (24 hours), configurable with `keep_jobs_seconds` in the master config.

## Checked

2026-11-09. Read in full the Salt Job Management page (doc/topics/jobs/index.rst, master branch): The jobs Runner (active, lookup_jid, list_jobs). Nothing removed.

Method: documentation only; no commands were run.
