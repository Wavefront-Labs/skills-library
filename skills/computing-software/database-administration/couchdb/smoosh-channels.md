---
id: computing-software.database-administration.couchdb.smoosh-channels
name: smoosh-channels
category: computing-software
field: database-administration
product: couchdb
tags: [smoosh, compaction, channels, ratio, slack]
level: advanced
status: docs-checked
description: "Configure smoosh compaction channels: ratio vs slack priority, min_priority, db_channels and view_channels, and the special upgrade and cleanup channels."
sources:
  - https://raw.githubusercontent.com/apache/couchdb/main/src/docs/src/maintenance/compaction.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A channel is a queue of pending compactions. Databases and views have separate channels, each channel is processed concurrently, and each has a set number of active compactions. Channels are local to a node.

Two channel types:

- **Ratio**: driven by `sizes.file / sizes.active`; compactions are queued when it exceeds `min_priority`, higher first.
- **Slack**: driven by `sizes.file - sizes.active`, with the same `min_priority` rule.

Channels are defined in `[smoosh.{channel-name}]` blocks and activated by naming them in `db_channels` or `view_channels`. Documented defaults:

```ini
[smoosh]
db_channels = upgrade_dbs,ratio_dbs,slack_dbs
view_channels = upgrade_views,ratio_views,slack_views
cleanup_channels = index_cleanup

[smoosh.ratio_dbs]
priority = ratio
min_priority = 2.0

[smoosh.slack_dbs]
priority = slack
min_priority = 536870912
```

The `upgrade` channels enqueue files whose `disk_format_version` is out of date (and views after a collation library upgrade). `index_cleanup` removes stale index files and purges `_local` checkpoint documents after design document updates.

## Checked

2026-11-04. Confirmed against the CouchDB maintenance/compaction page (Channels, Channel Configuration): ratio and slack formulas, min_priority, db_channels and view_channels, the documented default values, upgrade and index_cleanup channels. Nothing removed.

Method: documentation only; no commands were run.
