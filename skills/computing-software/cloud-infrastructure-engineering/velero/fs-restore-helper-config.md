---
id: computing-software.cloud-infrastructure-engineering.velero.fs-restore-helper-config
name: fs-restore-helper-config
category: computing-software
field: cloud-infrastructure-engineering
product: velero
tags: [restore-wait, pod-volume-restore, fs-restore-action-config, secctx, restore-helper]
level: advanced
status: docs-checked
description: "Customise the FSB restore helper init container image, resources and securityContext with a labelled ConfigMap."
sources:
  - https://velero.io/docs/main/file-system-backup/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
FSB restore adds a helper init container (named `restore-wait`) to restored pods. By default its image is the Velero server image. Override it, resources and security context with a ConfigMap in the Velero namespace, found by label:

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: fs-restore-action-config
  namespace: velero
  labels:
    velero.io/plugin-config: ""
    velero.io/pod-volume-restore: RestoreItemAction
data:
  image: myregistry.io/my-custom-helper-image[:OPTIONAL_TAG]
  cpuRequest: 200m
  memRequest: 128Mi
  cpuLimit: 200m
  memLimit: 128Mi
  secCtxRunAsUser: 1001
  secCtxRunAsGroup: 999
  secCtxAllowPrivilegeEscalation: false
```

Defaults: if the image has no tag the main Velero image tag is used; requests and limits for CPU default to 100m and for memory to 128Mi; a value of "0" means unbounded.

`secCtx` takes a YAML securityContext object (capabilities, readOnlyRootFilesystem, runAsUser, runAsGroup) and overrides the three `secCtx*` keys when its own runAsUser, runAsGroup or allowPrivilegeEscalation are set.

Use case: a restore stuck at `Init:0/1` because the volume root owner or mode blocks the helper. Set `secCtxRunAsUser` and `secCtxRunAsGroup` to match the workload UID and GID.

## Checked

2026-11-03. Read against the Velero docs (main): https://velero.io/docs/main/file-system-backup/. Confirmed the commands, flags, field names, defaults and limits stated above against those pages. Nothing was removed.

Method: documentation only; no commands were run.
