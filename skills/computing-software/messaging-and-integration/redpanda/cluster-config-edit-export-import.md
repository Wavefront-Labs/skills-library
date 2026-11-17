---
id: computing-software.messaging-and-integration.redpanda.cluster-config-edit-export-import
name: cluster-config-edit-export-import
category: computing-software
field: messaging-and-integration
product: redpanda
tags: [cluster-properties, rpk-cluster-config, export, import, lint, broker-properties, admin-api]
level: practitioner
status: docs-checked
description: "Change Redpanda cluster properties with rpk cluster config edit, check restart need, export and import between clusters, and lint redpanda.yaml."
sources:
  - https://docs.redpanda.com/streaming/current/manage/cluster-maintenance/cluster-property-configuration/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Cluster properties are stored internally and replicated to every broker; broker properties live in `/etc/redpanda/redpanda.yaml` on each broker. Topic-level properties override cluster-level ones.

**Edit**
1. On a broker run `rpk cluster config edit` (add `--all` to include tuning properties).
2. Edit and save. The Admin API validates, so a bad value such as `fetch_max_bytes` set to `5o` returns `expected type integer` and `No changes were made.`
3. On success it prints PRIOR and NEW per property and a new configuration version number ("Successfully updated configuration. New configuration version is 2.").
4. Check restart need with `rpk cluster config status`, which shows NODE, CONFIG-VERSION, NEEDS-RESTART, INVALID and UNKNOWN. Property descriptions say which ones need a restart.

`rpk cluster config set` also works but does not show the current value or description. View a value with `rpk cluster config get <property_name>`.

**Copy to another cluster**
```bash
rpk cluster config export --filename <filename>.yaml
rpk cluster config import --filename <filename>.yaml
```
Import applies the settings to all nodes in the target cluster. It does not import cluster-specific identification such as `cluster_id`.

**Stray cluster keys in redpanda.yaml.** If `redpanda.yaml` holds both kinds of properties, the cluster properties there are ignored. Remove them with:

```bash
rpk cluster config lint
```

On Kubernetes use the Kubernetes-specific cluster property page instead.

## Checked

2026-11-08. Read the whole Configure Cluster Properties page and confirmed cluster versus broker property storage, topic override, the edit flow with --all, the fetch_max_bytes validation example, PRIOR/NEW output and version number, rpk cluster config status columns, set versus edit, get, export and import, the cluster_id caution, and rpk cluster config lint. Nothing removed.

Method: documentation only; no commands were run.
