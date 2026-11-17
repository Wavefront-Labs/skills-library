---
id: computing-software.systems-network-administration.incus.incus-agent-vm
name: incus-agent-vm
category: computing-software
field: systems-network-administration
product: incus
tags: [incus, agent, vm, 9p, install-sh, exec, file, windows, freebsd]
level: advanced
status: docs-checked
description: "Install the Incus agent in a VM that lacks it so incus exec, incus file and usage metrics work: attach the agent drive, mount, run install.sh or install.ps1."
sources:
  - https://raw.githubusercontent.com/lxc/incus/main/doc/howto/instances_create.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Incus agent in VMs

The agent enables `incus exec`, `incus file` and detailed usage in `incus info`. VM images from the images remote already include it; install it by hand for others.

1. Either use the 9p mount in step 2, or attach the agent as a virtual CD-ROM, which must stay attached because it is read on every boot: `incus config device add INSTANCE-NAME agent disk source=agent:config`.
2. Linux, as root with systemd: `mount -t 9p config /mnt` (or `mount /dev/disk/by-label/incus-agent /mnt`), then `cd /mnt` and `./install.sh`.
3. Windows: run `install.ps1` from the CD-ROM as local administrator.
4. FreeBSD, macOS, NetBSD: 9p mount and `install.sh` as root. On FreeBSD use `-T` with `incus exec` for non-interactive commands.

## Checked

2026-11-04: confirmed against the Incus create-instances how-to, agent section (purpose, pre-installed on the images remote, 9p versus CD-ROM delivery, Linux/Windows/BSD/macOS install steps, FreeBSD `-T` note). Corrected: the CD-ROM drive is the alternative to the 9p mount, not a required first step.

Method: documentation only; no commands were run.
