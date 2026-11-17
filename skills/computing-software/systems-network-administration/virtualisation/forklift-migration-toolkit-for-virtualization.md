---
id: computing-software.systems-network-administration.virtualisation.forklift-migration-toolkit-for-virtualization
name: forklift-migration-toolkit-for-virtualization
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [forklift, migration-toolkit-for-virtualization, kubevirt, openshift-virtualization, v2v]
level: advanced
status: draft
description: "Migrate VMs from vSphere, oVirt, OpenStack or OVA to KubeVirt/OpenShift Virtualization with Forklift (MTV): providers, VDDK image, network and storage maps, warm migration."
sources:
  - https://docs.redhat.com/en/documentation/migration_toolkit_for_virtualization/
  - https://github.com/kubev2v/forklift
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Migration Toolkit for Virtualization (Forklift) to KubeVirt

**Goal:** move fleets of VMs into OpenShift Virtualization or upstream KubeVirt with planned, repeatable migrations.

## Install
- OpenShift: install the **Migration Toolkit for Virtualization** operator, create the `ForkliftController` CR (namespace `openshift-mtv`).
- Upstream: deploy Forklift with its operator on a KubeVirt cluster.

## Providers
- **VMware vSphere**: vCenter URL, credentials (read + snapshot privileges), CA cert, and a **VDDK image**: download the VDDK from Broadcom, build a small container image with it, push to your registry, reference it in the provider. Without VDDK, transfers are much slower or unsupported.
- oVirt/RHV, OpenStack, OVA (NFS share), other OpenShift Virtualization clusters.
- The destination provider is the local cluster.

## Maps and plan (CRDs)
```yaml
apiVersion: forklift.konveyor.io/v1beta1
kind: NetworkMap
spec:
  map:
    - source: { name: 'VM Network' }
      destination: { type: multus, namespace: vms, name: vlan20 }
---
kind: StorageMap
spec:
  map:
    - source: { name: datastore1 }
      destination: { storageClass: ocs-storagecluster-ceph-rbd }
---
kind: Plan
spec:
  warm: true
  targetNamespace: vms
  vms: [ { name: app01 }, { name: app02 } ]
```
Then a `Migration` CR (or *Start* in the console) runs it; for warm plans set the cutover time.

## Cold vs warm
- **Cold**: source powered off, disks copied, converted with virt-v2v, VM created.
- **Warm**: incremental copies using CBT snapshots while the source runs; at cutover the source is shut down, final delta copied, conversion runs. Enable CBT on source VMs first.

## Hooks and checks
Pre/post migration hooks run Ansible playbooks (for example to remove VMware Tools or update DNS). Validation flags unsupported configs (RDMs, shared disks, unsupported OS) before you start.

## Verify
`oc get plan,migration -n openshift-mtv` shows *Succeeded*; the VM runs in the target namespace with the mapped network, and the guest has virtio drivers and the QEMU guest agent.
