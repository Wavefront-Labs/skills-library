---
id: computing-software.cloud-infrastructure-engineering.talos-linux.vlan-interface-config
name: vlan-interface-config
category: computing-software
field: cloud-infrastructure-engineering
product: talos-linux
tags: [vlan, vlanconfig, 802-1q, networking, logical-link]
level: practitioner
status: docs-checked
description: "Configure a VLAN interface with a VLANConfig document: vlanID, vlanMode, parent link (physical or bond), naming, addresses and DHCP, with the exact YAML from the docs."
sources:
  - https://github.com/siderolabs/docs/blob/main/public/talos/v1.15/networking/logical/vlan.mdx
  - https://github.com/siderolabs/docs/blob/main/public/talos/v1.15/reference/configuration/network/vlanconfig.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A VLAN segments traffic on a shared physical network. In Talos a VLAN can sit on a physical interface or on another logical interface such as a bond.

Create a `VLANConfig` document:

```yaml
apiVersion: v1alpha1
kind: VLANConfig
name: enp0s3.2
vlanID: 2
vlanMode: 802.1q
parent: enp0s3
up: true
addresses:
    - address: 192.168.1.100/32
```

How the fields work:

- `name`: the VLAN interface name; `enp0s3.2` is a convention and can be customised.
- `vlanID`: the tag, here `2`.
- `vlanMode`: the tagging protocol; `802.1q` is the most common.
- `parent`: the underlying physical or logical interface the VLAN is created on.
- `up: true` brings the link up.

Addresses and routes are configured in the same document, exactly as for static link configuration; DHCP can be enabled on the VLAN interface as in dynamic link configuration.

## Checked

Both cited pages read. Dropped the VIP-on-VLAN and kernel command line remarks, which came from pages not cited.

Method: docs-checked 2026-11-09 against Talos v1.15 docs networking/logical/vlan.mdx and reference/configuration/network/vlanconfig.mdx.
