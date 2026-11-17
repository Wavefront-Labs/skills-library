---
id: computing-software.systems-network-administration.virtualisation.proxmox-package-repositories
name: proxmox-package-repositories
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [pve-repositories, pve-no-subscription, pve-enterprise, proxmox-installation, deb822, apt, ceph-repository, proxmox, proxmox-ve]
level: practitioner
status: docs-checked
description: "Set Proxmox VE apt repositories correctly: enterprise vs no-subscription vs test, Ceph repos, deb822 sources in PVE 9, the 401 error, and patching nodes safely."
sources:
  - https://pve.proxmox.com/pve-docs/chapter-sysadmin.html#sysadmin_package_repositories
  - https://github.com/proxmox/pve-docs/blob/master/pve-package-repos.adoc
  - https://github.com/proxmox/pve-docs/blob/master/system-software-updates.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Proxmox VE package repositories and updates

**Goal:** nodes pull updates from the right channel, and `apt` does not fail on a
repository you have no subscription for.

## Channels
| Repository | Use |
|---|---|
| `pve-enterprise` | Recommended; enabled by default; needs a valid subscription key for the node (keys are bound to the host architecture) |
| `pve-no-subscription` | Needs no key; the docs describe it for testing and non-production use |
| `pve-test` | Latest packages, primarily used by developers; testing only |
| Ceph (`enterprise`, `no-subscription`, `test` per Ceph release) | Only when installing Ceph for a hyper-converged cluster or connecting to an external cluster |
Plus the base Debian repositories (main, updates, security).

## Configure (GUI: node → Updates → Repositories; or files)
Repositories live in `/etc/apt/sources.list` (legacy single-line format) and in `.sources` files under `/etc/apt/sources.list.d/` (modern deb822 multi-line format); since Debian 13 Trixie apt complains about the legacy format. The current docs, for the Trixie based release, use deb822:
```
# /etc/apt/sources.list.d/proxmox.sources
Types: deb
URIs: http://download.proxmox.com/debian/pve
Suites: trixie
Components: pve-no-subscription
Signed-By: /usr/share/keyrings/proxmox-archive-keyring.gpg
```
The enterprise repository is shipped as `/etc/apt/sources.list.d/pve-enterprise.sources` (`URIs: https://enterprise.proxmox.com/debian/pve`, `Components: pve-enterprise`). Without a subscription key, deactivate it and configure `pve-no-subscription` instead. You always need the base Debian repositories in addition to a Proxmox VE repository.

## Updating
```sh
apt update && apt full-upgrade      # not plain apt upgrade
pveversion -v                       # package versions
```
Proxmox VE uses a rolling release model on top of Debian: `apt full-upgrade` can remove existing packages to satisfy dependencies, while `apt upgrade` cannot, so `apt upgrade` may leave a partially upgraded or broken package state. Regular updates are essential for security fixes. For live migration the target node must run the same or a newer version of the Proxmox VE packages, so update and test nodes one at a time.

## Gotchas
- Ceph repositories are per Ceph release (for example `ceph-squid`, `ceph-tentacle`); each Proxmox VE major release requires a corresponding minimum Ceph major release, and upgrading Ceph to its next major release follows the separate Ceph upgrade guide.
- The Ceph release table in the docs lists estimated end-of-life dates; check it before choosing a release.

## Verify
`apt update` completes with no errors; the node's Repositories panel in the GUI shows no warnings; `pveversion -v` shows the expected package versions on each node.

## Checked

2026-10-26 against the Proxmox VE admin guide sources (github.com/proxmox/pve-docs master, last commit 2026-10-17: pve-package-repos.adoc and system-software-updates.adoc, Trixie based release) and confirmed the repository names (pve-enterprise, pve-no-subscription, pve-test), their URIs, suites and components, the deb822 format and the Trixie legacy-format warning, the apt full-upgrade versus apt upgrade warning, and the Ceph repository structure. Corrected pvetest to pve-test and the enterprise URI; removed the unconfirmed PVE 8 .list example, the 401 error, cluster update order, Debian-mixing and JavaScript popup claims.

Method: documentation only; no commands were run.
