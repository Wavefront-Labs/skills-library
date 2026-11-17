---
id: computing-software.cloud-infrastructure-engineering.rook.object-store-deployment-scenarios
name: object-store-deployment-scenarios
category: computing-software
field: cloud-infrastructure-engineering
product: rook
tags: [cephobjectstore, rgw, s3, shared-pools, rados-namespaces, object-store-types]
level: practitioner
status: docs-checked
description: "Choose between local, shared-pool, placement-target, external, multisite and multi-instance object store layouts, and create a local S3 store."
sources:
  - https://rook.io/docs/rook/latest-release/Storage-Configuration/Object-Storage-RGW/object-storage/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Object storage exposes an S3 and/or Swift API for applications to put and get data. Rook offers several scenarios, and changing an object store's configuration from one type to another is not supported:
- Local object store with dedicated Ceph pools: recommended when one store is required; simplest to start.
- One or more stores with shared pools: recommended when several stores are needed.
- Stores with pool placement targets and storage classes, giving clients different placement options.
- A connection to an RGW service in an external Ceph cluster.
- RGW multisite to synchronize buckets between stores in different clusters.
- Multi-instance RGW: several CephObjectStores with different configurations on the same pools, for example separate instances for S3, Swift or the Admin-ops API.

Local S3 store: apply the sample CephObjectStore, which needs at least three OSDs on different nodes (`failureDomain: host`, with EC chunk settings of 2 data plus 1 coding). The operator creates all pools and resources, which may take about a minute. Confirm with:
```
kubectl -n rook-ceph get pod -l app=rook-ceph-rgw
```

Shared pools: create the shared pools once, then each store uses them. Data isolation between stores is enforced with RADOS namespaces, which do not allow cross-store access. There is only one `.rgw.root` pool for the metadata of all stores, so skip creating it if a store already exists. Check pods with `kubectl -n rook-ceph get pod -l rgw=store-a`; more stores need only a different CephObjectStore name.

## Checked

2026-11-03. Confirmed against the Object Storage page: the list of deployment scenarios, the no-conversion rule, the local store needing three OSDs, shared pools with RADOS namespace isolation and the single .rgw.root pool. Removed: nothing.

Method: documentation only; no commands were run.
