---
id: computing-software.systems-network-administration.virtualisation.proxmox-subscriptions-and-offline-mirror
name: proxmox-subscriptions-and-offline-mirror
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [proxmox-offline-mirror, pve-subscription, proxmox, apt-repositories]
level: practitioner
status: docs-checked
description: "Manage Proxmox VE subscription keys and run proxmox-offline-mirror for air-gapped hosts: mirror setup, snapshots, removable media sync and offline key activation."
sources:
  - https://pom.proxmox.com/installation.html
  - https://pom.proxmox.com/offline-keys.html
  - https://pom.proxmox.com/offline-mirror.html
  - https://pom.proxmox.com/offline-media.html
  - https://pom.proxmox.com/command-syntax.html
  - https://pve.proxmox.com/pve-docs/pve-admin-guide.html#sysadmin_package_repositories
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Subscriptions and proxmox-offline-mirror

**Goal:** licensed hosts get enterprise updates, including hosts with no internet access.

## Subscription keys (online)
```bash
pvesubscription set <key>                 # set this node's key
pvesubscription get                       # read subscription info
pvesubscription update --force            # always contact the server, even if the local cache is valid
```
A key is needed to use the `pve-enterprise` repository (`enterprise.proxmox.com`). Keys are bound to the host architecture: an arm64 host needs an arm64 key and an x86 key is not valid on it. Without a key, disable the enterprise repository (add `Enabled: no` to its entry) and use `pve-no-subscription` for testing and non-production use.

## Air-gapped: proxmox-offline-mirror
The tool needs a Debian-based host (physical, VM or container) with a 64-bit CPU, enough disk (the docs recommend at least 150 GiB for a basic Debian plus Proxmox VE mirror) and a file system that supports hard links, both locally and on the medium. FAT-style file systems do not.

To mirror an enterprise repository you need both an active product subscription key and a Proxmox Offline Mirror subscription. Offline activation needs pve-manager 7.2-11 or later on Proxmox VE.

On the internet-connected host:
```bash
apt update
apt install proxmox-offline-mirror
proxmox-offline-mirror setup                                  # wizard: pick the product, accept auto-adding the Debian base repos
proxmox-offline-mirror key add-mirror-key <pom-key>           # activates the mirroring system's own subscription
pvesubscription get                                           # on each PVE host: read its server ID
proxmox-offline-mirror key add <pve-key> <server-id>          # register a host key; fetches signed info from the shop
proxmox-offline-mirror mirror snapshot create <mirror-id>     # first run is slow and large
proxmox-offline-mirror config media add --id <medium-id> --mirrors <mirror-id> --sync true --verify-mode size --mountpoint <path>
proxmox-offline-mirror medium sync <medium-id>                # copies snapshots and offline keys to the medium
```
Config lives in `/etc/proxmox-offline-mirror.cfg` (override with `--config` or `PROXMOX_OFFLINE_MIRROR_CONFIG`). The wizard is the quickest route; `config mirror add` is the manual one, and a `base-dir` can be shared by Proxmox mirrors so common files are stored once.

On the offline PVE host, with the medium mounted, run `proxmox-offline-mirror-helper`:
```bash
proxmox-offline-mirror-helper setup                           # guided: choose mirrors and snapshots, writes a sources.list.d snippet (default offline-mirror.list)
proxmox-offline-mirror-helper offline-key --source <mountpoint-or-URL>   # activate or renew the subscription offline
apt update && apt full-upgrade
```
After the upgrade, disable or remove the snippet to avoid apt errors from automatic refresh.

## Alternatives
Serve the medium over HTTP inside the isolated network (the docs show an nginx example with `disable_symlinks off`) and use `deb [check-valid-until=false] http://<server>/<mirror-name>/<snapshot-timestamp> <suite> <components>`. `offline-key --source` accepts an HTTP URL, but the other helper commands need a local mount point.

## Gotchas
- Offline keys must be re-synced to the host at least once a year or before the key's next due date, whichever comes first.
- Snapshots are point-in-time and named by UTC timestamp. Use `mirror snapshot name` to give a stable alias, and `last` (the latest-snapshot symlink) exists only on the mirroring host.
- Removing or pruning snapshots does not free disk space until `mirror gc` runs (or `prune --gc`). Use `prune --dry-run` first; named snapshots are protected unless `--ignore-names` is given.
- `--verify-mode` is `none`, `size` or `full`; the docs recommend `size`.
- Proxmox debug symbol packages live in a separate repository (`dbgsym.proxmox.com`) and must be mirrored separately if wanted.

## Verify
`pvesubscription get` shows the offline-activated subscription on the target host; `apt update` reads only from the medium snippet; `pveversion -v` reaches the target version.

## Checked
Date: 2026-11-08. Confirmed against the Proxmox Offline Mirror pages (installation, offline keys, offline mirror, offline media, command syntax) and the Proxmox VE administration guide (package repositories, pvesubscription reference). Corrected: `key add` takes `<key> <server-id>`, the mirror key is added with `key add-mirror-key`; `snapshot create` and `medium sync` take a positional id; `offline-key` uses `--source`. Removed: socket-count matching of keys, the separate helper apt package line, the "Active" status wording, and the unsupported partial-mirror dependency claim.
Method: documentation only; no commands were run.
