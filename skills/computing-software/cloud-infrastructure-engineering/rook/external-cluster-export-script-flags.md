---
id: computing-software.cloud-infrastructure-engineering.rook.external-cluster-export-script-flags
name: external-cluster-export-script-flags
category: computing-software
field: cloud-infrastructure-engineering
product: rook
tags: [create-external-cluster-resources, rbd-data-pool-name, restricted-auth-permission, cephfs-filesystem-name, rgw-endpoint]
level: advanced
status: docs-checked
description: "Run create-external-cluster-resources.py on the provider cluster with the right flags for RBD, CephFS, RGW, monitoring and restricted users."
sources:
  - https://rook.io/docs/rook/latest-release/CRDs/Cluster/external-cluster/provider-export/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Run the script in the provider's cephadm shell, where it can create users and keys:
```
python3 create-external-cluster-resources.py --rbd-data-pool-name <pool_name> \
  --cephfs-filesystem-name <filesystem-name> --rgw-endpoint <rgw-endpoint> \
  --namespace <namespace> --format bash
```
Copy the bash output; it is pasted into the consumer shell later.

Flags from the page:
- `--namespace`: where the CephCluster runs, for example rook-ceph.
- `--rbd-data-pool-name`, with `--alias-rbd-data-pool-name` when the pool name contains a period or underscore.
- `--rgw-endpoint` as `<IP>:<PORT>` or `<FQDN>:<PORT>`, plus `--rgw-pool-prefix` (default `default`), `--rgw-tls-cert-path`, and `--rgw-skip-tls` (not recommended).
- `--cephfs-filesystem-name`, `--cephfs-metadata-pool-name`, `--cephfs-data-pool-name`, `--subvolume-group`, `--rados-namespace`.
- `--monitoring-endpoint`, `--monitoring-endpoint-port`, `--skip-monitoring-endpoint`.
- `--restricted-auth-permission`: limits CSI users to specific pools; requires `--rbd-data-pool-name` and `--k8s-cluster-name`, and optionally the CephFS filesystem name.
- `--dry-run`, `--output`, `--run-as-user` (prefixed `client.`), `--config-file` (command line beats config.ini beats defaults).
- `--v1-port-enable`: use mon port 6789 instead of the default v2 port 3300.
- `--cephx-key-rotate` and `--cephx-key-type` (`aes` or `aes256k`).
- `--upgrade` refreshes the CSI keyrings and `client.healthchecker` with new permissions while keeping older ones.
- `--topology-pools` and related flags are covered in the topology-based provisioning page.

Run with `--dry-run` first to print the commands without executing them.

## Checked

2026-11-03. Read the Rook docs page(s) cited in sources (provider-export) against this skill: 36 backticked identifiers, flags, versions and quoted strings were matched to the page text; the 0 reported as not literally matched are YAML nesting or placeholder formatting, and each was confirmed by reading the surrounding page text (nested field lists, example output, command blocks). Nothing needed removing.

Method: documentation only; no commands were run.
