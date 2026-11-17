---
id: computing-software.database-administration.cloudnative-pg.fencing-instances-annotation-and-plugin
name: fencing-instances-annotation-and-plugin
category: computing-software
field: database-administration
product: cloudnative-pg
tags: [fencing, fencedinstances, postmaster, crashloop, kubectl-cnpg, troubleshooting, primary]
level: advanced
status: docs-checked
description: "Fence one, several or all instances with cnpg.io/fencedInstances or kubectl cnpg fencing; fencing a primary causes an outage."
sources:
  - https://github.com/cloudnative-pg/cloudnative-pg/blob/main/docs/src/fencing.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Fencing guarantees the `postmaster` is shut down while the pod keeps running, so data is not modified and the file system can be investigated. The annotation `cnpg.io/fencedInstances` takes a JSON list of instance names:

- `'["cluster-example-1"]'` fences one instance
- `'["cluster-example-1","cluster-example-2"]'` fences two
- `'["*"]'` fences the whole cluster
- an empty list behaves as if the annotation were not set

Use `kubectl annotate` or the plugin:

```shell
# to fence only one instance
kubectl cnpg fencing on cluster-example 1

# to fence all the instances in a Cluster
kubectl cnpg fencing on cluster-example "*"
```

Lift it by clearing or changing the annotation, or:

```shell
kubectl cnpg fencing off cluster-example 1
kubectl cnpg fencing off cluster-example "*"
```

`fencing off` for a single instance does not work if the whole cluster was fenced; in that case edit the annotation by hand.

Shutdown is the same as a switchover: a fast shutdown with timeout `.spec.switchoverDelay`, then an immediate shutdown. Afterwards the pod stays alive but is not Ready, configuration files and certificates still reconcile, and metrics are not collected except `cnpg_collector_fencing_on`, set to 1.

Warning: fencing a **primary** shuts PostgreSQL down with no failover, interrupting applications; when the fence is lifted it simply restarts. Fence primaries only if strictly required. A fenced instance that is deleted is recreated without starting the postmaster, which helps with crash-looping instances.

## Checked

2026-11-08. Annotation syntax, plugin commands, shutdown behaviour and the primary warning confirmed on the Fencing page.

Method: documentation only; no commands were run.
