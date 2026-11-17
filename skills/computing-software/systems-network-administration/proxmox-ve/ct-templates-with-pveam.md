---
id: computing-software.systems-network-administration.proxmox-ve.ct-templates-with-pveam
name: ct-templates-with-pveam
category: computing-software
field: systems-network-administration
product: proxmox-ve
tags: [lxc, pveam, container-template, vztmpl]
level: intro
status: docs-checked
description: "Download and manage LXC container templates on Proxmox VE with pveam and create a container from one with pct create."
sources:
  - https://pve.proxmox.com/pve-docs/chapter-pct.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Container templates are tar archives used to create LXC containers. They can be downloaded in the GUI or with `pveam` (Proxmox VE Appliance Manager), which fetches from the Proxmox repositories.

```
pveam update
pveam available
pveam available --section system
pveam download local debian-10.0-standard_10.0-1_amd64.tar.gz
pveam list local
pveam remove local:vztmpl/debian-10.0-standard_10.0-1_amd64.tar.gz
```

The list of available templates is refreshed daily by the pve-daily-update timer; run `pveam update` to refresh it manually. The `--section system` filter limits output to the plain operating system templates. Downloaded templates live on the chosen storage under the `vztmpl` content type, which is why they are referenced as `local:vztmpl/<file>`.

Create a container from a downloaded template with `pct create`, giving a unique CTID (IDs below 100 are reserved for internal use and IDs are unique cluster wide):

```
pct create 100 local:vztmpl/debian-10.0-standard_10.0-1_amd64.tar.gz
pct start 100
```

Substitute the real template file name from `pveam list`. The chapter also describes OCI images as a technology preview, so prefer standard system templates for production containers.

After creation use `pct config 100` to review the generated configuration, which is stored in `/etc/pve/lxc/100.conf` and replicated to all cluster nodes.

## Checked

2026-11-09. Compared with the Container Images, OCI Images and Configuration sections of https://pve.proxmox.com/pve-docs/chapter-pct.html. The pct create and pct start lines follow the chapter's usage; the template file name is the chapter's example.

Method: documentation only; no commands were run.

