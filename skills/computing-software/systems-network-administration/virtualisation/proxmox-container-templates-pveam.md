---
id: computing-software.systems-network-administration.virtualisation.proxmox-container-templates-pveam
name: proxmox-container-templates-pveam
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [pveam, container-template, pct, pct-create, lxc, oci-image, vztmpl, proxmox, proxmox-ve]
level: practitioner
status: docs-checked
description: "Create Proxmox LXC containers from templates: pveam update/available/download, pct create with storage, network and features, custom templates, and OCI images in PVE 9."
sources:
  - https://pve.proxmox.com/pve-docs/pve-admin-guide.html#pct_container_images
  - https://pve.proxmox.com/pve-docs/pveam.1.html
  - https://pve.proxmox.com/pve-docs/pct.1.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Container templates and pct create

**Goal:** lightweight Linux system containers created from trusted templates, scripted.

## Templates
```sh
pveam update
pveam available --section system | grep -E 'debian|ubuntu|alma|rocky'
pveam download local <template-file-name>
pveam list local
```
Templates are stored as `vztmpl` content (`local:vztmpl/...`). `pveam available --section` accepts `mail`, `system` and `turnkeylinux`; the template list is refreshed daily by pve-daily-update and on demand with `pveam update`. Containers can also be created from OCI images pulled from a registry or uploaded to a storage; running application containers is a technology preview.

## Create
```sh
pct create 200 local:vztmpl/<template-file-name> \
  --hostname dns01 --cores 2 --memory 1024 --swap 512 \
  --rootfs local-lvm:8 --net0 name=eth0,bridge=vmbr0,tag=20,ip=10.0.20.53/24,gw=10.0.20.1 \
  --unprivileged 1 --features nesting=1 --ssh-public-keys /root/ops.pub \
  --onboot 1 --start 1
pct config 200
pct enter 200          # root shell inside
pct exec 200 -- apt update
```

## Custom templates
Build a container, configure it, remove machine-specific state, stop it, then **Convert to template** (`pct template 200`) for clones, or back it up with vzdump and restore the archive with `pct restore` to create new containers.

## Gotchas
- `ostype` selects the OS-specific setup PVE applies inside the container (network, hostname); `unmanaged` skips it, and the setting can also be forced to `unmanaged` to disable all modifications. Container start fails if a configured ostype differs from the auto-detected one.
- Keep templates updated; containers created from old templates start with old packages.
- Containers share the host kernel: kernel modules and some sysctls cannot be set from
  inside.

## Verify
`pct list` shows the container running; `pct exec 200 -- ip a` shows the intended IP;
SSH with the key works.

## Checked

2026-10-26 against the Proxmox VE admin guide sources (github.com/proxmox/pve-docs master, last commit 2026-10-17: pct.adoc Container Images, pveam synopsis, pct create and restore options) and confirmed the pveam subcommands and --section values, the vztmpl volume syntax, the pct create options used (--rootfs, --net0, --unprivileged, --features, --ssh-public-keys, --onboot, --start) and ostype/unmanaged behaviour. Replaced the pinned template file name with a placeholder.

Method: documentation only; no commands were run.
