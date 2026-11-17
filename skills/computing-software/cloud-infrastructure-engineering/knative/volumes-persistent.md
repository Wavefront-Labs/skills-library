---
id: computing-software.cloud-infrastructure-engineering.knative.volumes-persistent
name: volumes-persistent
category: computing-software
field: cloud-infrastructure-engineering
product: knative
tags: [volumes, persistent-volume-claim, podspec-persistent-volume-claim, config-features, empty-dir]
level: practitioner
status: docs-checked
description: "Mount emptyDir, secret, configMap, projected and PVC volumes after enabling the feature flags."
sources:
  - https://knative.dev/docs/serving/services/storage/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: give Knative Services data storage.

Serving can mount these volume types: `emptyDir`, `secret`, `configMap` and `projected`. PersistentVolumes are supported but need a feature flag. Warning: mounting large volumes may add considerable start-up time.

Enable PVCs in the `config-features` ConfigMap:

```bash
kubectl patch --namespace knative-serving configmap/config-features \
 --type merge \
 --patch '{"data":{"kubernetes.podspec-persistent-volume-claim": "enabled", "kubernetes.podspec-persistent-volume-write": "enabled"}}'
```

- `kubernetes.podspec-persistent-volume-claim` controls whether persistent volumes can be used with Knative Serving at all.
- `kubernetes.podspec-persistent-volume-write` controls whether they are available with write access.

If you installed Serving with the Knative Operator, set these flags only in the corresponding Serving custom resource.

Then reference the volume in the Service:

```yaml
spec:
  template:
    spec:
      containers:
        - image: ...
          volumeMounts:
            - mountPath: /data
              name: mydata
      volumes:
        - name: mydata
          persistentVolumeClaim:
            claimName: knative-pv-claim
            readOnly: false
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: knative-pv-claim
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 1Gi
```

The claim is a normal Kubernetes PersistentVolumeClaim, here one gigabyte with `ReadWriteOnce` access.

## Checked

Method: docs-checked 2026-11-09 against https://knative.dev/docs/serving/services/storage/ (read in full; patch command, flag meanings, operator note and example all match).
