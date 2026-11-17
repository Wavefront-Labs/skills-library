---
id: computing-software.cloud-infrastructure-engineering.velero.restore-change-image-names
name: restore-change-image-names
category: computing-software
field: cloud-infrastructure-engineering
product: velero
tags: [change-image-name, image-repository, restore-image-mapping, restoreitemaction, registry-migration]
level: practitioner
status: docs-checked
description: "Rewrite container image names during a Velero restore with the velero.io/change-image-name ConfigMap and comma-separated substring pairs."
sources:
  - https://velero.io/docs/main/restore-reference/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Velero can change the image name of pods, deployments, statefulsets, daemonsets, replicasets, replicationcontrollers, jobs and cronjobs during a restore. Create a ConfigMap in the Velero namespace:

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: change-image-name-config
  namespace: velero
  labels:
    velero.io/plugin-config: ""
    velero.io/change-image-name: RestoreItemAction
data:
  "case1": "1.1.1.1:5000,2.2.2.2:3000"
  "case2": "dev/,test/"
```

Any name can be used for the ConfigMap; Velero identifies it by the two labels, which must be used verbatim. Each value is `<old_image_name_sub_part><delimiter><new_image_name_sub_part>`. In the current implementation the delimiter can only be a comma. Keys can be any words ConfigMap accepts.

Matching is on a part of the image name, so these all work for the old image `1.1.1.1:5000/abc:test`:
- `1.1.1.1:5000,2.2.2.2:3000` swaps the registry.
- `5000,3000` swaps a port only.
- `abc:test,edf:test` swaps a repository and tag.
- `1.1.1.1:5000/abc:test,2.2.2.2:3000/edf:test` swaps the whole name.

Gotcha from the docs: an image name may contain more than one part that matches the replacing words. To change `dev/image1:dev` and `dev/image2:dev` to `test/image1:dev` and `test/image2:dev`, use `dev/,test/`, which avoids an unexpected replacement of the second "dev".

## Checked

Checked 2026-11-08 against the Velero Restore Reference page ("Changing Image Repositories", read in full). Removed unsourced advice: the test-on-one-namespace procedure (including `--include-namespaces` and `kubectl get pod`), cleanup of the ConfigMap, and the registry-migration motivation sentence.

Method: documentation only; no commands were run.
