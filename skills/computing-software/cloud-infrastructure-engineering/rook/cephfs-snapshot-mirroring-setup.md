---
id: computing-software.cloud-infrastructure-engineering.rook.cephfs-snapshot-mirroring-setup
name: cephfs-snapshot-mirroring-setup
category: computing-software
field: cloud-infrastructure-engineering
product: rook
tags: [filesystem-mirroring, cephfilesystemmirror, fs-peer-token, snapshot-mirror, peer-bootstrap]
level: sme
status: docs-checked
description: "Mirror a CephFS to a peer cluster: enable mirroring in the CephFilesystem CR, import the fs-peer-token, then verify daemon and snapshot sync status."
sources:
  - https://rook.io/docs/rook/latest-release/Storage-Configuration/Shared-Filesystem-CephFS/filesystem-mirroring/
  - https://rook.io/docs/rook/latest-release/CRDs/Shared-Filesystem/ceph-fs-mirror-crd/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
CephFS mirroring is configured in the `mirroring` section of the CephFilesystem CR and run by a `CephFilesystemMirror` daemon.

CephFilesystem `mirroring` fields:
- `enabled`: default false.
- `peers.secretNames`: peers to connect to; only a single peer (one Ceph cluster) is supported.
- `snapshotSchedules`: one or more, each with `path`, `interval` (d, h or m suffix) and optional `startTime` in ISO 8601.
- `snapshotRetention`: retention policy with a `path`.

Bootstrap the peer. Rook creates a token secret such as `fs-peer-token-myfs`:
```
kubectl get secret -n rook-ceph fs-peer-token-myfs -o jsonpath='{.data.token}'|base64 -d
```
Save the decoded value to a file on the destination and import it:
```
ceph fs snapshot mirror peer_bootstrap import <fs_name> <token file path>
```
Then configure a directory for snapshot mirroring as described in the CephFS mirror documentation.

Verify from the toolbox with `ceph fs snapshot mirror daemon status | jq`. For deeper checks exec into `deploy/rook-ceph-fs-mirror`, find the `ceph-client.fs-mirror` admin socket under `/var/run/ceph`, and run `ceph --admin-daemon <socket> fs mirror status myfs@1`.

## Checked

2026-11-03. Read the Rook docs page(s) cited in sources (filesystem-mirroring, ceph-fs-mirror-crd) against this skill: 18 backticked identifiers, flags, versions and quoted strings were matched to the page text; the 2 reported as not literally matched are YAML nesting or placeholder formatting, and each was confirmed by reading the surrounding page text (nested field lists, example output, command blocks). Nothing needed removing.

Method: documentation only; no commands were run.
