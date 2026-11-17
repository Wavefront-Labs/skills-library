---
id: computing-software.cloud-infrastructure-engineering.opa-gatekeeper.opa-gatekeeper-data-sync-syncset-and-config
name: opa-gatekeeper-data-sync-syncset-and-config
category: computing-software
field: cloud-infrastructure-engineering
product: opa-gatekeeper
tags: [opa-gatekeeper, sync, syncset, config, data-inventory, referential-policy, synconly]
level: advanced
status: docs-checked
description: "Replicate cluster objects into Gatekeeper for referential policies using SyncSet (recommended) or the Config syncOnly list, then read them from data.inventory."
sources: ["https://github.com/open-policy-agent/gatekeeper/blob/master/website/docs/sync.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Opa gatekeeper data sync syncset and config

Some policies need more than the object under test, for example checking that a label is unique across pods needs all other pods. Gatekeeper replicates chosen kinds into its data client.

SyncSet (v3.15+, alpha, recommended):

```yaml
apiVersion: syncset.gatekeeper.sh/v1alpha1
kind: SyncSet
metadata:
  name: syncset-1
spec:
  gvks:
    - {group: "", version: "v1", kind: "Namespace"}
    - {group: "", version: "v1", kind: "Pod"}
```

Config (v3.6+, alpha): a singleton named exactly `config` in `gatekeeper-system` (other names are ignored) with `spec.sync.syncOnly` listing the same group/version/kind entries.

The union of all SyncSet `gvks` and the Config `syncOnly` is synced. Editing them updates what is synced dynamically, and a resource stays cached while any of them still lists it.

Read replicated data in templates from `data.inventory`:
- cluster-scoped: `data.inventory.cluster[<groupVersion>][<kind>][<name>]`
- namespaced: `data.inventory.namespace[<namespace>][<groupVersion>][<kind>][<name>]`

When `--audit-from-cache=true`, an object must be in this cache before audit can evaluate it.

## Checked

2026-11-08. Confirmed against sync.md, read in full: SyncSet example and v3.15+ alpha, Config v3.6+ alpha named config, union semantics, dynamic updates, data.inventory paths, audit-from-cache note. Removed or corrected: nothing.

Method: documentation only; no commands were run.
