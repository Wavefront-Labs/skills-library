---
id: computing-software.cloud-infrastructure-engineering.saltstack.returners-job-cache-and-events
name: returners-job-cache-and-events
category: computing-software
field: cloud-infrastructure-engineering
product: saltstack
tags: [saltstack, returners, master-job-cache, external-job-cache, event-return, prep-jid]
level: advanced
status: docs-checked
description: "Make a Salt returner serve as the master job cache or external job cache, the functions required, testing with the ret module, and event_return."
sources:
  - https://raw.githubusercontent.com/saltstack/salt/master/doc/ref/returners/index.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Returners as job cache and event sink

**Master job cache** (`master_job_cache`): a returner can replace the default job cache. Required functions:
- `prep_jid`: generate or accept a unique job ID.
- `save_load`: store job data.
- `get_load`: fetch job data by ID, or an empty dict if not found.

**External job cache** builds on it and adds `get_jid`, `get_fun`, `get_jids` and `get_minions` for querying stored jobs and minions. Test them with the `ret` execution module:

```
salt-call ret.get_jids <returner>
```

**Event returners**: set the `event_return` master option to log master events to one or more returners. The returner must provide `event_return(events)`. Not every returner supports it, and busy masters can see many events per second, so watch storage capacity.

## Checked

2026-11-09. Read against the returners source (doc/ref/returners/index.rst); required functions, the ret test commands and the event_return notes were confirmed there. Nothing removed.
Method: documentation only; no commands were run.
