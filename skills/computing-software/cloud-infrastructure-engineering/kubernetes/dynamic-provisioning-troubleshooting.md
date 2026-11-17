---
id: computing-software.cloud-infrastructure-engineering.kubernetes.dynamic-provisioning-troubleshooting
name: dynamic-provisioning-troubleshooting
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, dynamic-provisioning, storageclass, csi, external-provisioner, provisioningfailed, waitforfirstconsumer, quota, topology, troubleshooting, pvc-pending, ebs-csi, gce-pd-csi, azure-disk-csi]
level: advanced
status: docs-checked
description: "Debugging a PVC stuck Pending under dynamic provisioning: the exact event chain to read, and the common root causes behind each failure."
sources: ["https://kubernetes.io/docs/concepts/storage/dynamic-provisioning/", "https://kubernetes.io/docs/concepts/storage/storage-classes/", "https://kubernetes.io/docs/concepts/storage/storage-capacity/", "https://kubernetes.io/docs/concepts/policy/resource-quotas/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dynamic provisioning troubleshooting

**Goal:** read the events in order to find why a PVC stays `Pending`.

## 1. Triage order
```bash
kubectl describe pvc <name> -n <ns>
kubectl get storageclass <class> -o yaml
kubectl get events -n <ns> --field-selector involvedObject.name=<pvc-name>
```
Check which class the PVC uses. A PVC without `storageClassName` gets the default class (the one annotated `storageclass.kubernetes.io/is-default-class`); setting `storageClassName: ""` explicitly disables dynamic provisioning for it. If events show nothing, check that the CSI controller (external-provisioner sidecar) is running and that the class `provisioner` matches the registered driver name (`kubectl get csidriver`).

## 2. Common causes
- **Waiting for first consumer.** `volumeBindingMode: WaitForFirstConsumer` delays binding and provisioning until a Pod using the PVC is created. It is not a failure; if the Pod is Pending too, debug scheduling.
- **Provisioning errors from the driver.** The external-provisioner event repeats the driver's error. Read the controller Pod logs of both the `csi-provisioner` sidecar and the driver container; the sidecar says that it failed, the driver says why (permissions, quotas, invalid parameters).
- **Topology.** With `Immediate` binding on topology-constrained storage, volumes are provisioned without knowing where the Pod will run, which can leave Pods unschedulable; use `WaitForFirstConsumer` (and `allowedTopologies` only if still required).
- **ResourceQuota.** A namespace quota (including per-class keys such as `<class-name>.storageclass.storage.k8s.io/requests.storage`) can reject the claim.
- **Wrong or legacy provisioner name.** A StorageClass naming a provisioner that is not installed never provisions.
- **Capacity tracking.** If the driver publishes `CSIStorageCapacity` objects, the scheduler may refuse nodes without enough reported capacity, producing a scheduling event about storage rather than a provisioning event (`kubectl get csistoragecapacity -A`).
## 3. Logs
```bash
kubectl logs -n <csi-namespace> <controller-pod> -c csi-provisioner
kubectl logs -n <csi-namespace> <controller-pod> -c <driver-container>
```

## Verify
- [ ] The Pending PVC is attributed to one of: scheduling, quota, topology, driver permission or capacity, or StorageClass configuration, with the event or log line as evidence.
- [ ] Both the sidecar and driver logs were read.
- [ ] `WaitForFirstConsumer` Pending was recognised as normal when no Pod used the PVC.

## Checked

Checked 2026-10-26 against Kubernetes website docs (main branch, latest commit 2026-10-25, covering Kubernetes 1.36) plus the named upstream project docs and Kubernetes source. Confirmed: default class and empty storageClassName behaviour, WaitForFirstConsumer, Immediate-binding topology caveat, per-class ResourceQuota keys, CSIStorageCapacity.

Method: documentation only; no commands were run.
