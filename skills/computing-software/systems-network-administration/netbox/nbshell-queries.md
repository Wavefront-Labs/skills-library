---
id: computing-software.systems-network-administration.netbox.nbshell-queries
name: nbshell-queries
category: computing-software
field: systems-network-administration
product: netbox
tags: [nbshell, django-queryset, lsmodels]
level: advanced
status: docs-checked
description: "Query and modify objects directly with the preloaded Django shell."
sources: ["https://netboxlabs.com/docs/netbox/administration/netbox-shell/", "https://netboxlabs.com/docs/netbox/administration/management-commands/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# NetBox shell

Goal: inspect or fix data directly.

```
cd /opt/netbox
source /opt/netbox/venv/bin/activate
python3 netbox/manage.py nbshell
```

This is a lightly customized Django shell with NetBox models preloaded. The stock shell is `manage.py shell`. The banner reports the Python, Django and NetBox versions and notes that `lsapps()` and `lsmodels()` list available models; `help(<model>)` gives details. Exit with `exit()` or Ctrl+D.

**Querying.** Use a Django queryset. The base form is `<model>.objects.all()`, which shows a truncated list of all objects of that type, for example `Device.objects.all()`.

**Related commands.** The management commands page documents `reindex`, `calculate_cached_counts` and `rebuild_prefixes`; check it before reaching for a shell.

**Danger.** The shell gives direct access to NetBox data and functions with very little validation. Only authorized, knowledgeable users should ever have it. Never act in the shell without a full backup in place. Bulk ORM methods such as `bulk_create()` and `update()` bypass model validation; call `full_clean()` before `save()`.

**Checklist**

1. Activate the venv.
2. Use `lsmodels()` to discover names.
3. Restrict who can open it.

## Checked

Method: docs-checked 2026-11-09 against the NetBox Python Shell page and the Management Commands page (both read in full). Removed the unconfirmed claim that the API and scripts write change-log records.
