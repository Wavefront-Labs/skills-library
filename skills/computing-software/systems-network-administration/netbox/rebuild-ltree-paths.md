---
id: computing-software.systems-network-administration.netbox.rebuild-ltree-paths
name: rebuild-ltree-paths
category: computing-software
field: systems-network-administration
product: netbox
tags: [ltree-paths, hierarchical-models, sort-path]
level: sme
status: docs-checked
description: "Check then rebuild ltree path columns for regions, locations and other trees."
sources: ["https://netboxlabs.com/docs/netbox/administration/management-commands/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Repairing hierarchical paths

Goal: fix `path` and `sort_path` columns on tree models.

`rebuild_ltree_paths` recomputes both columns for hierarchical models: regions, site groups, locations, device roles, platforms, tenant groups, contact groups, wireless LAN groups, module bays, inventory items and inventory item templates. With no arguments it covers all of them; or name `app_label.ModelName`.

**Check first**

```
python3 netbox/manage.py rebuild_ltree_paths --check
```

It compares each object's stored paths with its parent's, reports models that disagree and modifies nothing. It takes no locks, so it is safe on a live system or replica. Counts show whether a model needs rebuilding, not how many objects are wrong.

**Rebuild**

```
python3 netbox/manage.py rebuild_ltree_paths dcim.region
```

Paths are derived by walking down from roots, so objects no root reaches (cycles, self-parented, or pointing at a missing parent) cannot be repaired. The command raises a `CommandError` listing those rows; fix their parent relationships and re-run.

A rebuild rewrites every row of each model in one statement, locking rows until commit. Use a maintenance window and avoid concurrent hierarchy changes.

**Checklist**

1. Run `--check` first.
2. Fix unreachable rows.
3. Schedule the rebuild.

## Checked

Method: docs-checked 2026-11-09 against the NetBox Management Commands page (rebuild_ltree_paths section, read in full).
