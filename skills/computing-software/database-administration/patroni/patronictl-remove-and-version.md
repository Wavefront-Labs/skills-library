---
id: computing-software.database-administration.patroni.patronictl-remove-and-version
name: patronictl-remove-and-version
category: computing-software
field: database-administration
product: patroni
tags: [patroni, patronictl, remove, version, dcs]
level: practitioner
status: docs-checked
description: "Delete a cluster's state from the DCS with patronictl remove and check versions with patronictl version."
sources:
  - https://patroni.readthedocs.io/en/latest/patronictl.html
  - https://patroni.readthedocs.io/en/latest/existing_data.html
  - https://patroni.readthedocs.io/en/latest/dcs_failsafe_mode.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: wipe Patroni state deliberately and verify versions.

`patronictl remove CLUSTER [--group N] [-f pretty|tsv|json|yaml]` removes all cluster information from the DCS. It is interactive and destroys Patroni cluster state. The documented prompts are:
1. Confirm the cluster name.
2. Type the phrase `Yes I am aware`.
3. If the cluster is healthy, also give the leader name.

The format option controls how members are printed while prompting (default pretty). It is part of the documented major-upgrade procedure, where the `initialize` key must be removed (or the whole cluster state wiped with `patronictl remove`) because pg_upgrade runs initdb, which creates a new system identifier.

`patronictl version [CLUSTER...] [MEMBER...] [--group N]`:

```
patronictl -c postgres0.yml version batman
patronictl version 4.0.0
postgresql0: Patroni 4.0.0 PostgreSQL 16.4
```

With no arguments it prints only the patronictl version; with a cluster it lists each member's Patroni and PostgreSQL versions; with member names it lists only those members.

Before enabling `failsafe_mode`, the docs say to ensure the Patroni version on all members is up to date, which `patronictl version` helps check.

## Checked

2026-11-08. Confirmed against the Patroni patronictl page (remove and version sections), the convert-standalone page (major upgrade steps) and the DCS failsafe mode page (enabling note).

Method: documentation only; no commands were run.
