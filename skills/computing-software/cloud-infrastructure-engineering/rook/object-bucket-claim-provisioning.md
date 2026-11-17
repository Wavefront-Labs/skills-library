---
id: computing-software.cloud-infrastructure-engineering.rook.object-bucket-claim-provisioning
name: object-bucket-claim-provisioning
category: computing-software
field: cloud-infrastructure-engineering
product: rook
tags: [objectbucketclaim, obc, generatebucketname, bucket-storageclass, additionalconfig, bucketpolicy]
level: practitioner
status: docs-checked
description: "Request buckets with an ObjectBucketClaim: name rules, storage class behaviour, the generated Secret and ConfigMap, and quota options."
sources:
  - https://rook.io/docs/rook/latest-release/Storage-Configuration/Object-Storage-RGW/ceph-object-bucket-claim/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
An Object Bucket Claim (OBC) requests a new or existing bucket. An Object Bucket (OB) is generated when a bucket is provisioned; it is a global resource, typically not visible to non-admins. An admin-created StorageClass names the provisioner and object store, decides new versus existing bucket, and sets the retention policy.

When an OBC appears, the Ceph provisioner creates the bucket or grants access, then writes a Secret with credentials and a ConfigMap with the endpoint. Both take the OBC name; pods consume them. To watch only the cluster namespace, set `ROOK_OBC_WATCH_OPERATOR_NAMESPACE` to true in the operator manifest, otherwise all namespaces are watched. The provisioner name defaults to the operator namespace prefix; `ROOK_OBC_PROVISIONER_NAME_PREFIX` in `rook-ceph-operator-config` customizes it, but changing it on existing clusters is unsupported.

Naming:
- `bucketName` is not recommended for new buckets since names are unique in the whole store. If another owner already has it, the OBC stays Pending, with the reason in the operator log.
- `generateBucketName` is a random-name prefix; leave `bucketName` empty (`bucketName` wins if both are set).
- If both are blank, the storage class must name an existing bucket; all three blank is an error.

`additionalConfig` options: `maxObjects` and `maxSize` (quota on the auto-created user; minimum recommended 4K), and disabled-by-default `bucketMaxObjects`, `bucketMaxSize` and `bucketPolicy` (raw JSON).

## Checked

2026-11-03. Read the Rook docs page(s) cited in sources (ceph-object-bucket-claim) against this skill: 11 backticked identifiers, flags, versions and quoted strings were matched to the page text; the 0 reported as not literally matched are YAML nesting or placeholder formatting, and each was confirmed by reading the surrounding page text (nested field lists, example output, command blocks). Nothing needed removing.

Method: documentation only; no commands were run.
