---
id: computing-software.systems-network-administration.virtualisation.proxmox-major-version-upgrade
name: proxmox-major-version-upgrade
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [pve-upgrade, pve8to9, pve7to8, proxmox-upgrade, dist-upgrade, proxmox-installation, proxmox, proxmox-ve, debian]
level: advanced
status: docs-checked
description: "In-place Proxmox VE 8 to 9 upgrade: prerequisites, pve8to9 checker, Ceph Squid first, Trixie repositories, dist-upgrade per node, reboot and the known upgrade issues."
sources:
  - https://pve.proxmox.com/wiki/Upgrade_from_8_to_9
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Proxmox VE 8 to 9 in-place upgrade

**Goal:** move each node from Proxmox VE 8.4 (Debian Bookworm) to 9.x (Debian Trixie) with
apt, node by node. The 7 to 8 wiki page was not reviewed; follow it directly for that hop.

## Prerequisites (from the wiki page)
- Latest Proxmox VE 8.4 on all nodes (`pveversion` at least 8.4.1 after
  `apt update` and `apt dist-upgrade`); fix repositories first if pve-manager is older.
- Hyper-converged Ceph: Quincy or Reef clusters must be on Ceph 19.2 Squid before the
  upgrade (`ceph --version`). Co-installed Proxmox Backup Server has its own 3 to 4 how-to.
- Host-independent access (IKVM/IPMI or physical); if only SSH, test on identical
  non-production hardware and use tmux or screen. Do not upgrade from the GUI virtual console.
- A healthy cluster, valid tested backups of all VMs and CTs, and at least 5 GB free on
  the root mount point, ideally more than 10 GB. Check the known upgrade issues first.
- Third-party packages and repositories must also be compatible with Debian Trixie.

## Run the checker
`pve8to9` (included in the latest 8.4 packages) gives hints and warnings; `pve8to9 --full`
enables all checks and should be run at least once before upgrading. It only reports and
changes nothing. Re-run it after each fix, and again after the upgrade.

## Per node
1. Migrate away any VMs and CTs that must keep running. Migrating from older to newer
   Proxmox VE always works; newer to older may work but is generally not supported.
2. Switch repositories to Trixie, for example
   `sed -i 's/bookworm/trixie/g' /etc/apt/sources.list` and the same for
   `/etc/apt/sources.list.d/pve-enterprise.list`; leave no Bookworm entries. Add the
   Proxmox VE 9 repository in deb822 style (Suites `trixie`, Components `pve-enterprise` or
   `pve-no-subscription`), run `apt update` and `apt policy`, then remove the old repository
   files. For Ceph use `ceph-squid` with Suites `trixie`; a 401 error may need
   `pvesubscription update --force`. Remove any backports line.
3. `apt update`, then `apt dist-upgrade`. Expect prompts about configuration files:
   keep your version of `/etc/issue`; take the maintainer's version of `/etc/lvm/lvm.conf`
   if you made no changes; inspect `/etc/ssh/sshd_config`, `/etc/default/grub` (choose "No"
   if unsure) and `/etc/chrony/chrony.conf`. Duration depends on the root filesystem: a slow
   spinner can take 60 minutes or more, fast SSD servers under 5 minutes.
4. Re-run `pve8to9`, then reboot into the new kernel, even if you already ran 6.14 before.
5. Clear the browser cache. Once every node is on the latest packages, HA groups migrate
   automatically to HA rules; check `journalctl -eu pve-ha-crm` on the active CRM node if
   problems appear.

## Known issues the page names (check them before you start)
- Upgrade wants to remove `proxmox-ve`: on Proxmox VE installed over plain Debian,
  `apt remove linux-image-amd64` first.
- Kernel audit messages: optionally `systemctl disable --now systemd-journald-audit.socket`
  before upgrading.
- Third-party storage plugins: wait for the plugin author.
- Ceph "insecure key types" HEALTH_ERR can appear after the first MON node reboots; the
  page says resume the upgrade and migrate the keys afterwards.
- Interface names can change with the new kernel; Proxmox VE 9 has a
  `pve-network-interface-pinning` tool.
- Ceph full-mesh setups with `post-up /usr/bin/systemctl restart frr.service` can deadlock
  on boot; change to the page's `is-active ... || true` form before rebooting.
- LVM thin pool may need `lvconvert --repair pve/data`; LVM autoactivation is disabled for
  new LVs and the page offers `/usr/share/pve-manager/migrations/pve-lvm-disable-autoactivation`.
- cgroup v1 is gone; containers with systemd 230 or older are unsupported.
- `/etc/sysctl.conf` is no longer read; move settings to `/etc/sysctl.d/<NN>-<name>.conf`.
- Veeam backups break for VMs on QEMU machine version 10.0 or higher; pin 9.2+pve1 or
  postpone.
- Live migration between different CPU models or vendors can cause problems.

## Troubleshooting
For a partial upgrade after a network failure run `apt -f install`. The warning
"You are attempting to remove the meta-package 'proxmox-ve'" means a package cannot be
upgraded because its Trixie repository is not configured.

## Checked
Date: 2026-11-07. Read the whole Proxmox wiki page "Upgrade from 8 to 9" (oldid 12639).
Every command, path, size and version above is on it. Removed as not on the page: the
7 to 8 content (second source dropped, page not opened), `ha-manager crm-command
node-maintenance`, `pveversion -v`, `systemctl --failed`, `pvecm status`, ".link file"
interface pinning (the page names the pinning tool instead), the "mixed-version for weeks"
advice, the DKMS remark and the test-VM migration Verify step. The new-installation
procedure and the remaining known issues (GRUB on LVM in UEFI, systemd-boot meta-package,
NVIDIA vGPU, FRR fabrics, PCI passthrough, memory display) were left out, not unconfirmed.
Method: documentation only; no commands were run.
