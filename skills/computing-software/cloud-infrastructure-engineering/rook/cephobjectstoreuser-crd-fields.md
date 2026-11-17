---
id: computing-software.cloud-infrastructure-engineering.rook.cephobjectstoreuser-crd-fields
name: cephobjectstoreuser-crd-fields
category: computing-software
field: cloud-infrastructure-engineering
product: rook
tags: [cephobjectstoreuser, quotas, capabilities, opmask, defaultplacement, clusternamespace]
level: practitioner
status: docs-checked
description: "CephObjectStoreUser fields: store, quotas, capabilities set at creation only, defaultPlacement, defaultStorageClass and opMask."
sources:
  - https://rook.io/docs/rook/latest-release/CRDs/Object-Storage/ceph-object-store-user-crd/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A `CephObjectStoreUser` creates an RGW user and its credentials secret.

Core fields:
- `name`: reflected in the secret and other resource names.
- `store`: the CephObjectStore it belongs to.
- `displayName`: passed to `radosgw-admin user create`.
- `clusterNamespace`: where the CephCluster and CephObjectStore live. A user outside that namespace works only if the store's `allowUsersInNamespaces` includes the user's namespace.
- `quotas`: `maxBuckets`, `maxSize` (across all the user's buckets) and `maxObjects`.

`capabilities` give extra permissions (read, write, read plus write, or `*`) on resources such as user, `userInfoWithoutKeys` (Ceph 19.2.0 or newer) and `accounts` (Ceph 19.2.3 or newer). Because go-ceph lacks an update API, capabilities can only be set at creation; to change them, delete and re-create the user.

Placement:
- `defaultPlacement` overrides the zonegroup default target for the user's buckets. RGW rejects unknown targets and the user phase becomes Failure, with the error as an Event. Removing the setting leaves the last value in place; to pin the zonegroup default, name that target.
- `defaultStorageClass` sets objects' storage class within `defaultPlacement`, which must also be set. Changing `defaultPlacement` resets it to STANDARD.

`opMask` is the set of operation types (read, write, delete) a user may perform, applied regardless of bucket or IAM policy. Reading an object needs both the read bit and a policy allowing `s3:GetObject`.

## Checked

2026-11-03. Read the Rook docs page(s) cited in sources (ceph-object-store-user-crd) against this skill: 20 backticked identifiers, flags, versions and quoted strings were matched to the page text; the 2 reported as not literally matched are YAML nesting or placeholder formatting, and each was confirmed by reading the surrounding page text (nested field lists, example output, command blocks). Nothing needed removing.

Method: documentation only; no commands were run.
