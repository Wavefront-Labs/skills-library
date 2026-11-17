---
id: computing-software.systems-network-administration.proxmox-ve.disable-ksm-memory-merging
name: disable-ksm-memory-merging
category: computing-software
field: systems-network-administration
product: proxmox-ve
tags: [ksm, ksmtuned, allow-ksm, memory-dedup, side-channel]
level: practitioner
status: docs-checked
description: "Check and disable Kernel Samepage Merging on a Proxmox VE node or for a single VM."
sources:
  - https://pve.proxmox.com/pve-docs/chapter-sysadmin.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
KSM deduplicates identical memory pages across VMs and is enabled by default. It can lower memory use when many VMs run similar guests, but it exposes VMs to side-channel attacks: research has shown that information about one VM can be inferred from a second VM on the same host by exploiting KSM behaviour. If you provide hosting services, consider disabling it, and check your country's regulations because disabling may be a legal requirement.

Check whether it is active on a node:

```
systemctl status ksmtuned
```

Disable it on the node and unmerge pages that are already merged:

```
systemctl disable --now ksmtuned
echo 2 > /sys/kernel/mm/ksm/run
```

Disable it for one VM with the `allow-ksm` option, which defaults to true:

```
qm set <vmid> --allow-ksm 0
```

## Checked

Checked 2026-11-08 against the Kernel Samepage Merging section of the pve-docs sysadmin chapter (partial read of a long page). Confirmed the default, side-channel risk, hosting and regulation advice, ksmtuned check and disable, unmerge command and allow-ksm option. Removed the unsourced trade-off advice paragraph.

Method: documentation only; no commands were run.
