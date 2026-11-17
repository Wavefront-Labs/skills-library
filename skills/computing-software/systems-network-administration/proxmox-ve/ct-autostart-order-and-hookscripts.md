---
id: computing-software.systems-network-administration.proxmox-ve.ct-autostart-order-and-hookscripts
name: ct-autostart-order-and-hookscripts
category: computing-software
field: systems-network-administration
product: proxmox-ve
tags: [lxc, startup-order, onboot, hookscript]
level: practitioner
status: docs-checked
description: "Control container start order and delays with the startup option, and attach a hookscript to a Proxmox VE container."
sources:
  - https://pve.proxmox.com/pve-docs/chapter-pct.html
  - https://pve.proxmox.com/pve-docs/pct.conf.5.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Containers can start automatically at host boot with `onboot`, and the `startup` option shapes ordering:

```
pct set 100 --onboot 1
pct set 100 --startup order=1,up=30,down=60
```

`order` is a non-negative number giving the general startup order. Shutdown uses the reverse order, so a container with order 1 starts first and stops last. `up` is the delay in seconds before the next guest is started after this one, and `down` is the delay before the next guest is stopped. Guests without an order value always start after those that have one, and the ordering only applies between guests on the same host. The default shutdown timeout is 60 seconds.

Hookscripts run at lifecycle phases of a container. Attach one stored in a snippets directory on a storage:

```
pct set 100 -hookscript local:snippets/hookscript.pl
```

An example script ships on the host at `/usr/share/pve-docs/examples/guest-example-hookscript.pl`, so copy that as a starting point. The snippets content type must be enabled on the storage that holds the script.

For anything that cannot be done through supported options, `lxc.*` keys may be written directly into the container config and are passed to the low level LXC tools. Use that sparingly, since such settings bypass the managed options.

## Checked

2026-11-03. Commands, option names, defaults, limits and behaviour claims were compared with the official Proxmox VE documentation pages: https://pve.proxmox.com/pve-docs/chapter-pct.html, https://pve.proxmox.com/pve-docs/pct.conf.5.html (plus the chapter-qm, qm.1, pct, pvecm, pvesm, vzdump, pvesr and sysadmin pages). Items shown as placeholder or example values (file names, VM IDs, device names) are illustrative. Figures that the pages did not state were removed or reworded.

Method: documentation only; no commands were run.
