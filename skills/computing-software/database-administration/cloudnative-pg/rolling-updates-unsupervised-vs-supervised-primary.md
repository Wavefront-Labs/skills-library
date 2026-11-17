---
id: computing-software.database-administration.cloudnative-pg.rolling-updates-unsupervised-vs-supervised-primary
name: rolling-updates-unsupervised-vs-supervised-primary
category: computing-software
field: database-administration
product: cloudnative-pg
tags: [rolling-update, primaryupdatestrategy, primaryupdatemethod, switchover, restart, supervised, unsupervised]
level: practitioner
status: docs-checked
description: "Control CloudNativePG rolling updates: triggers, replicas first, primaryUpdateStrategy and primaryUpdateMethod (restart or switchover)."
sources:
  - https://github.com/cloudnative-pg/cloudnative-pg/blob/main/docs/src/rolling_update.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Rolling updates start when you change `imageName`, the extension images in `.spec.postgresql.extensions`, an image catalog entry for the cluster's major version, a configuration change that needs a restart, `.spec.resources`, or the operator version (instance manager upgrade, unless in-place updates are enabled).

Replicas are upgraded one pod at a time, highest serial first; the **primary is always last**. Pods are recreated with the same PVCs, so no re-cloning happens, and service endpoints move away from the pod being updated.

`primaryUpdateStrategy`:

- `unsupervised` (default): fully automatic. After the replicas, the `primaryUpdateMethod` runs on the primary.
- `supervised`: the update pauses once all replicas are done. Finish it with a manual switchover or an in-place restart. An image upgrade cannot be applied by restart, so a switchover is required there.

```bash
kubectl cnpg promote [cluster] [new_primary]
kubectl cnpg restart [cluster] [current_primary]
```

`primaryUpdateMethod`:

- `restart` (default): restart the primary pod if possible, otherwise the request is ignored and a switchover is issued.
- `switchover`: promote the most aligned replica and shut down the old primary pod. The promoted instance already runs the target image, whereas `restart` may have to pull the image after the primary is down.

Warning: with `switchover` you cannot change the image name and PostgreSQL parameters in the same update; the operator rejects it with a validation error. Do them sequentially, waiting for the first rollout to finish.

## Checked

2026-11-08. Read in full: docs/src/rolling_update.md. Triggers, ordering, strategy and method options and the switchover validation warning confirmed on the Rolling updates page.

Method: documentation only; no commands were run.
