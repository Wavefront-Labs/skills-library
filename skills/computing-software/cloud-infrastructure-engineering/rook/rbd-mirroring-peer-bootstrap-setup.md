---
id: computing-software.cloud-infrastructure-engineering.rook.rbd-mirroring-peer-bootstrap-setup
name: rbd-mirroring-peer-bootstrap-setup
category: computing-software
field: cloud-infrastructure-engineering
product: rook
tags: [rbd-mirroring, bootstrap-peer, rbd-primary-site-secret, journal-based, snapshot-based, volumereplication]
level: sme
status: docs-checked
description: "Set up RBD mirroring between two Rook clusters: same-named mirrored pools, exchanging pool-peer-token secrets, rbd-mirror daemon and the CSI replication sidecars."
sources:
  - https://rook.io/docs/rook/latest-release/Storage-Configuration/Block-Storage-RBD/rbd-mirroring/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
RBD mirroring replicates images asynchronously between Ceph clusters in two modes: journal-based (each write is journaled and replayed remotely) and snapshot-based (periodic or manual mirror snapshots give crash-consistent copies).

Steps, repeated on each peer cluster:
1. Create a mirroring-enabled pool by adding `spec.mirroring` to the CephBlockPool and `kubectl create -f pool-mirrored.yaml`. The pool name must be identical on both peers. Existing pools can be edited to enable it.
2. Bootstrap peers. On the remote cluster find the secret name:
```
kubectl get cephblockpool.ceph.rook.io/mirrored-pool -n rook-ceph -ojsonpath='{.status.info.rbdMirrorBootstrapPeerSecretName}'
```
It is `pool-peer-token-mirrored-pool`. Decode its token, then on the other cluster create a secret with `kubectl -n rook-ceph create secret generic rbd-primary-site-secret --from-literal=token=<token> --from-literal=pool=mirrored-pool`. Repeat in the other direction.
3. Deploy the rbd-mirror daemon from `mirror.yaml` (`kubectl create -f mirror.yaml -n rook-ceph`), check a `rook-ceph-rbd-mirror-a` pod runs, and check health with `kubectl get cephblockpools.ceph.rook.io mirrored-pool -n rook-ceph -o jsonpath='{.status.mirroringStatus.summary}'`.
4. Add the peer to the pool:
```
kubectl -n rook-ceph patch cephblockpool mirrored-pool --type merge -p '{"spec":{"mirroring":{"peers": {"secretNames": ["rbd-primary-site-secret"]}}}}'
```
5. Create the VolumeReplication and VolumeReplicationClass CRDs from kubernetes-csi-addons on all peers, and enable the `csi-omap-generator` and `csi-addons` sidecars in the RBD provisioner pods, which are off by default.

## Checked

2026-11-03. Read the Rook docs page(s) cited in sources (rbd-mirroring) against this skill: 17 backticked identifiers, flags, versions and quoted strings were matched to the page text; the 0 reported as not literally matched are YAML nesting or placeholder formatting, and each was confirmed by reading the surrounding page text (nested field lists, example output, command blocks). Nothing needed removing.

Method: documentation only; no commands were run.
