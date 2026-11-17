---
id: computing-software.data-science-and-analytics.apache-superset.query-history-pruning
name: query-history-pruning
category: computing-software
field: data-science-and-analytics
product: apache-superset
tags: [prune-query, query-history, celery-beat, retention, sql-lab]
level: practitioner
status: draft
description: "Keep the Superset Query table small by scheduling the prune_query Celery beat task and choosing a retention window."
sources:
  - https://github.com/apache/superset/blob/master/docs/admin_docs/configuration/configuring-superset.mdx
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
Goal: stop SQL Lab query history from growing without bound.

Superset records every SQL Lab run in the metadata database Query table. Prune it with the periodic `prune_query` task, scheduled through Celery beat in `CeleryConfig.beat_schedule`:

```python
from celery.schedules import crontab

class CeleryConfig(object):
    beat_schedule = {
        "prune_query": {
            "task": "prune_query",
            "schedule": crontab(minute=0, hour=0, day_of_month=1),
            "options": {"retention_period_days": 180},
        },
    }
```

Notes:
- `retention_period_days` sets how old a row must be before deletion.
- The schedule only runs if a Celery beat process and at least one worker are running with this config; run only one beat.
- The same `beat_schedule` dict holds the other periodic jobs (reports scheduler, log pruning), so add the entry rather than replacing the dict.
- Choose retention against your audit needs; deleted history cannot be recovered except from metadata database backups.

Related: event logs have their own pruning (`reports.prune_log` for report execution logs).
