---
id: computing-software.systems-network-administration.incus.cloud-init-network-config
name: cloud-init-network-config
category: computing-software
field: systems-network-administration
product: incus
tags: [incus, cloud-init, network-config, netplan, ifupdown, static-ip, nocloud-net]
level: practitioner
status: docs-checked
description: "Set Incus instance networking via cloud-init.network-config: default DHCP on eth0, a static v2 example, and where files land."
sources:
  - https://raw.githubusercontent.com/lxc/incus/main/doc/cloud-init.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# cloud-init network configuration

- Default: cloud-init runs a DHCP client on `eth0`. The `network-config` option (`cloud-init.network-config`, or `user.network-config` on older images) overrides it.
- cloud-init renders the result via `ifupdown` (`/etc/network/interfaces.d/50-cloud-init.cfg`) or `netplan` (`/etc/netplan/50-cloud-init.yaml`) depending on the distribution.

```yaml
config:
  cloud-init.network-config: |
    version: 2
    ethernets:
      eth1:
        addresses:
          - 10.10.101.20/24
        gateway4: 10.10.101.1
        nameservers:
          addresses:
            - 10.10.10.254
```

Where data lands in the instance: `/var/lib/cloud/instance/cloud-config.txt`, `/var/lib/cloud/instance/user-data.txt`, `/var/lib/cloud/seed/nocloud-net/network-config`.

VM images relying on the agent need seed files in `/var/lib/cloud/seed/nocloud-net/` (`meta-data`, `network-config`, `user-data`, `vendor-data`); the agent applies them on first boot and reboots the VM.

## Checked

2026-11-09. Confirmed against the Incus doc cloud-init.md (How to specify network configuration data, cloud-init and virtual machines): default DHCP on eth0, ifupdown or netplan rendering, file paths, the example and the agent seed files. Removed: nothing needed removing.

Method: documentation only; no commands were run.
