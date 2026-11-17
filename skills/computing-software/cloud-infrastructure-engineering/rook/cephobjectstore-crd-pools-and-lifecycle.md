---
id: computing-software.cloud-infrastructure-engineering.rook.cephobjectstore-crd-pools-and-lifecycle
name: cephobjectstore-crd-pools-and-lifecycle
category: computing-software
field: cloud-infrastructure-engineering
product: rook
tags: [cephobjectstore, metadatapool, datapool, preservepoolsondelete, allowusersinnamespaces, defaultrealm]
level: advanced
status: docs-checked
description: "CephObjectStore pool settings and lifecycle fields: replicated metadata, EC data, preservePoolsOnDelete, allowUsersInNamespaces and defaultRealm."
sources:
  - https://rook.io/docs/rook/latest-release/CRDs/Object-Storage/ceph-object-store-crd/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Pool settings accept everything in the CephBlockPool spec.
- `metadataPool`: settings for all object store metadata pools. Must use replication.
- `dataPool`: the data pool, which can be replicated or erasure coded. An EC example with 2 data and 1 coding chunk needs at least three hosts and three devices.
- When the `zone` section is set, pools named after the object store are not created; the store uses the pools made by the CephObjectZone.
- `preservePoolsOnDelete`: when true the supporting pools stay after the store is deleted, protecting against accidental loss. Default false.

Access and realm fields:
- `allowUsersInNamespaces`: namespaces permitted to hold a CephObjectStoreUser for this store when the user is outside the Rook cluster namespace. Use "*" for all. Useful for apps needing credentials in their own namespace when neither OBCs nor COSI create the buckets. Default empty.
- `defaultRealm`: when true, marks the store's realm as the default realm in the cluster. Only one realm can be default, and Ceph does not let the default become unassigned once set; a different realm may be marked default instead.

Other top-level sections are `auth` (Keystone), `protocols`, and `gateway` for the RGW daemon. Those are covered in separate skills.

## Checked

2026-11-03. Confirmed against the CephObjectStore CRD page: metadataPool must be replicated, dataPool replicated or EC with the 2+1 example needing three hosts, zone behaviour, preservePoolsOnDelete default false, allowUsersInNamespaces and defaultRealm. Removed: nothing.

Method: documentation only; no commands were run.
