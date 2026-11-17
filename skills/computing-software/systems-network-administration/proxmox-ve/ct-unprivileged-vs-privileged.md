---
id: computing-software.systems-network-administration.proxmox-ve.ct-unprivileged-vs-privileged
name: ct-unprivileged-vs-privileged
category: computing-software
field: systems-network-administration
product: proxmox-ve
tags: [lxc, unprivileged, user-namespaces, nesting]
level: practitioner
status: docs-checked
description: "Choose between unprivileged and privileged LXC containers on Proxmox VE and know what nesting, keyctl and fuse features expose."
sources:
  - https://pve.proxmox.com/pve-docs/chapter-pct.html
  - https://pve.proxmox.com/pve-docs/pct.conf.5.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Unprivileged containers are the default when creating a container. They use user namespaces, so root (UID 0) inside the container maps to an unprivileged user outside it. Most container escapes or resource abuse then affect only a random unprivileged user, and the LXC team regards them as safe by design. If the container runs systemd, the version inside must be 220 or newer.

Privileged containers rely on AppArmor, seccomp filters and namespaces. The LXC team considers them unsafe and will not treat new escape exploits as CVE-worthy, so use them only in trusted environments.

The `unprivileged` option should not be modified manually after creation. On restore the default comes from the backup.

Advanced capabilities are set with `features`:

```
pct set 100 --features nesting=1,keyctl=1
```

- `nesting` (default 0) allows nested containers, is best used with unprivileged containers plus additional id mapping, and exposes host procfs and sysfs contents to the guest. systemd also needs it to isolate services.
- `keyctl` (default 0, unprivileged only) allows the keyctl() system call, required to run docker inside a container.
- `mknod` is experimental and needs seccomp trap to user space support (kernel 5.3 or newer).
- `fuse` allows FUSE mounts, but the docs strongly advise against FUSE inside containers because the kernel freezer breaks suspend and snapshot mode backups.

## Checked

2026-11-03. Commands, option names, defaults, limits and behaviour claims were compared with the official Proxmox VE documentation pages: https://pve.proxmox.com/pve-docs/chapter-pct.html, https://pve.proxmox.com/pve-docs/pct.conf.5.html (plus the chapter-qm, qm.1, pct, pvecm, pvesm, vzdump, pvesr and sysadmin pages). Items shown as placeholder or example values (file names, VM IDs, device names) are illustrative. Figures that the pages did not state were removed or reworded.

Method: documentation only; no commands were run.
