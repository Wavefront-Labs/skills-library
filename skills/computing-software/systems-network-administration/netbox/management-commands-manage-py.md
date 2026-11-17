---
id: computing-software.systems-network-administration.netbox.management-commands-manage-py
name: management-commands-manage-py
category: computing-software
field: systems-network-administration
product: netbox
tags: [management-commands, manage-py, calculate-cached-counts]
level: practitioner
status: docs-checked
description: "Use manage.py inside the virtualenv for repair and maintenance tasks."
sources: ["https://netboxlabs.com/docs/netbox/administration/management-commands/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Management commands

Goal: run built-in maintenance tools safely.

```
cd /opt/netbox
source /opt/netbox/venv/bin/activate
python3 netbox/manage.py <command>
```

Add `--help` to any command for its arguments.

**Commands described in the docs**

- `calculate_cached_counts`: recalculate cached counter fields such as a site's device count. Counters stay current automatically; this repairs drift.
- `nbshell`: Django shell with all NetBox models imported.
- `populate_image_sizes`: fill cached sizes for attachments predating the `image_size` field; recommended once after upgrade with many attachments on remote storage such as S3.
- `rebuild_config_context_cache`: pre-render merged config context for devices and VMs. `upgrade.sh` runs it. By default only empty caches render; add `--force` to refresh populated ones.
- `rebuild_prefixes`: recalculate prefix depth and child counts.
- `rebuild_ltree_paths`: repair hierarchical path columns.
- `reindex`: rebuild the search index, optionally for named apps or models.

Run through the virtualenv Python so dependencies load.

**Checklist**

1. Activate the venv.
2. Read `--help` first.
3. Run heavy rebuilds in a maintenance window.

## Checked

2026-11-03: confirmed against the cited NetBox documentation: Management commands page: calculate_cached_counts, nbshell, populate_image_sizes, rebuild_config_context_cache (--force), rebuild_prefixes, rebuild_ltree_paths, reindex. Removed: Nothing.

Method: documentation only; no commands were run.
