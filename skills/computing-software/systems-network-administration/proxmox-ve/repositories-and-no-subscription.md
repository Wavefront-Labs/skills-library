---
id: computing-software.systems-network-administration.proxmox-ve.repositories-and-no-subscription
name: repositories-and-no-subscription
category: computing-software
field: systems-network-administration
product: proxmox-ve
tags: [repositories, no-subscription, apt, deb822, enterprise]
level: intro
status: docs-checked
description: "Configure Proxmox VE apt repositories, switching from the enterprise repo to pve-no-subscription in deb822 .sources files."
sources:
  - https://pve.proxmox.com/pve-docs/chapter-sysadmin.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Proxmox VE uses APT. Repositories live in `/etc/apt/sources.list` (legacy single-line format) and in `.sources` files under `/etc/apt/sources.list.d/` (deb822 format). On Debian 13 Trixie apt complains about the legacy format; migrate with `apt modernize-sources`. Always keep the base Debian repositories in addition to a Proxmox one.

The `pve-enterprise` repository is enabled by default and needs a valid subscription key (keys are bound to the host architecture). Without a key, either add `Enabled: no` to its entry in `/etc/apt/sources.list.d/pve-enterprise.sources` or accept the error, then configure `pve-no-subscription` in `/etc/apt/sources.list.d/proxmox.sources`:

```
Types: deb
URIs: http://download.proxmox.com/debian/pve
Suites: trixie
Components: pve-no-subscription
Signed-By: /usr/share/keyrings/proxmox-archive-keyring.gpg
```

The no-subscription repository is for testing and non-production use because its packages are less heavily validated. The `pve-test` component is for developers testing new features. Debug symbols come from a separate `pve-dbgsym` repository.

Ceph has its own `ceph.sources` file with enterprise, no-subscription and test components per release (for example ceph-tentacle). Since Proxmox VE 9 the installer enables the Debian `non-free-firmware` component by default for early microcode updates.

Release files are GnuPG signed; the ISO already ships the keyring, while installs on top of Debian must fetch `proxmox-archive-keyring-trixie.gpg` into `/usr/share/keyrings/proxmox-archive-keyring.gpg`. The web UI Repository panel under the node shows repository state.

## Checked

2026-11-03. Commands, option names, defaults, limits and behaviour claims were compared with the official Proxmox VE documentation pages: https://pve.proxmox.com/pve-docs/chapter-sysadmin.html (plus the chapter-qm, qm.1, pct, pvecm, pvesm, vzdump, pvesr and sysadmin pages). Items shown as placeholder or example values (file names, VM IDs, device names) are illustrative. Figures that the pages did not state were removed or reworded.

Method: documentation only; no commands were run.
