---
id: computing-software.cloud-infrastructure-engineering.seaweedfs.seaweed-up-ssh-deploy
name: seaweed-up-ssh-deploy
category: computing-software
field: cloud-infrastructure-engineering
product: seaweedfs
tags: [cluster-yaml, ssh-deployment, rolling-upgrade, seaweed-up, ssh-deploy]
level: practitioner
status: docs-checked
description: "Deploy and operate bare-metal SeaweedFS clusters with seaweed-up: cluster.yaml topology, check, deploy, status, upgrade, scale in, destroy."
sources:
  - https://github.com/seaweedfs/seaweedfs/wiki/Deployment-with-seaweed-up
  - https://github.com/seaweedfs/seaweedfs/wiki/Cluster-Plan-Day-2-Operations
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# seaweed up ssh deploy

`seaweed-up` is an SSH-based deployer for Linux hosts driven by one YAML topology. It needs passwordless (or sudo-with-password) SSH and a user that can write to its install directories.

Install: download the release tarball (`seaweed-up_linux_amd64.tar.gz`) and put the binary in your PATH, or build with `go build`.

Core commands:
```bash
seaweed-up cluster check   -f cluster.yaml -u root -i /path/to/key
seaweed-up cluster deploy prod -f cluster.yaml -u root -i /path/to/key --yes
seaweed-up cluster status prod --json
seaweed-up cluster upgrade prod --version 4.19
seaweed-up cluster stop|start prod --component filer
seaweed-up cluster scale in prod --remove-node 10.0.0.13 --yes
seaweed-up cluster destroy prod --remove-data --yes
seaweed-up cluster prepare prod        # ulimits, sysctls, firewall, time sync
```
`check` is a preflight (SSH, sudo, disk, ports, time skew, arch). Upgrades are rolling with per-host health gates and rollback; scale-in drains volumes safely.

Generate `cluster.yaml` from a smaller `inventory.yaml` with `seaweed-up cluster plan -i inventory.yaml -o cluster.yaml`. Re-running appends new hosts byte-for-byte safely; `--dry-run` previews changes.

Verify: `cluster status` shows master, volume and filer probes healthy.

## Checked
Checked 2026-11-09: the SSH and sudo prerequisite, tarball install, every command in the core list, the preflight contents, rolling upgrade with health gates and rollback, safe scale-in, and the `cluster plan` append-merge and `--dry-run` behaviour match both pages. Nothing removed.
Method: docs-checked 2026-11-09 against the SeaweedFS wiki pages Deployment-with-seaweed-up and Cluster-Plan-Day-2-Operations, both read in full from a local clone of the wiki.
