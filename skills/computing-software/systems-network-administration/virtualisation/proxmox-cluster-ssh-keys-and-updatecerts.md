---
id: computing-software.systems-network-administration.virtualisation.proxmox-cluster-ssh-keys-and-updatecerts
name: proxmox-cluster-ssh-keys-and-updatecerts
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [pve-ssh-keys, pvecm-updatecerts, proxmox, cluster, ssh]
level: practitioner
status: docs-checked
description: "Fix Proxmox VE cluster SSH key and known_hosts problems that break migration and replication, and regenerate node certificates with pvecm updatecerts."
sources:
  - https://pve.proxmox.com/pve-docs/pvecm.1.html
  - https://pve.proxmox.com/pve-docs/pve-admin-guide.html#_role_of_ssh_in_proxmox_ve_clusters
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cluster SSH keys and pvecm updatecerts

**Goal:** nodes trust each other over SSH so migration, replication and the web shell work.

## How it is wired
- Root's `authorized_keys` is shared via pmxcfs: `/root/.ssh/authorized_keys` links to `/etc/pve/priv/authorized_keys`.
- Host keys of the cluster members are kept in `/etc/pve/priv/known_hosts`. Older systems may have `/etc/ssh/ssh_known_hosts` symlinked to it; `pvecm updatecerts --unmerge-known-hosts` removes that legacy setup.

## Typical breakage
After reinstalling a node with the same name, or changing its IP, migration fails with *Host key verification failed* or *REMOTE HOST IDENTIFICATION HAS CHANGED*.

## Fix
On the reinstalled/changed node and then on the others:
```bash
pvecm updatecerts                  # on the re-added node: updates its fingerprint cluster wide
pvecm updatecerts --force          # also forces generation of a new SSL certificate
```
The admin guide says to run `pvecm updatecerts` once on the re-added node after rejoining with the same IP or hostname. Keys of a removed node stay in `/etc/pve/priv/authorized_keys` until you delete them.
Restart the web proxy if the certificate changed: `systemctl restart pveproxy`.

## Gotchas
- Do not replace `/root/.ssh/authorized_keys` with a regular file; config management tools that do so break the cluster symlink.
- `pvecm updatecerts --silent` ignores errors such as a cluster without quorum.

## Verify
`ssh -o BatchMode=yes root@<ip> hostname` works between all pairs; a test migration succeeds.

## Checked
2026-11-01. Confirmed in the `pvecm` manual and the Proxmox VE admin guide: authorized_keys link to `/etc/pve/priv/authorized_keys`, `/etc/pve/priv/known_hosts`, `pvecm updatecerts` options (`--force`, `--silent`, `--unmerge-known-hosts`), the rejoin advice. Removed: HostKeyAlias, per-node known_hosts files, PermitRootLogin and pveproxy-ssl.pem claims.
Method: documentation only; no commands were run.
