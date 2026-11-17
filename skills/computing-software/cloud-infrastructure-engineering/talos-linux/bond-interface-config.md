---
id: computing-software.cloud-infrastructure-engineering.talos-linux.bond-interface-config
name: bond-interface-config
category: computing-software
field: cloud-infrastructure-engineering
product: talos-linux
tags: [bond, bondconfig, lacp, 802-3ad, link-aggregation, networking]
level: practitioner
status: docs-checked
description: "Create a bond (NIC teaming) with a BondConfig document: bond name, member links, mode, LACP and hash options, addresses, MTU and MAC, and matching the switch."
sources:
  - https://github.com/siderolabs/docs/blob/main/public/talos/v1.15/networking/logical/bond.mdx
  - https://github.com/siderolabs/docs/blob/main/public/talos/v1.15/reference/configuration/network/bondconfig.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A bond combines several physical interfaces into one logical interface for bandwidth and redundancy. If a member fails, traffic is redistributed over the remaining ones. The bond settings must match the switch configuration.

Create a `BondConfig` document:

```yaml
apiVersion: v1alpha1
kind: BondConfig
name: agg.0
links:
    - enp0s2
    - enp0s3
bondMode: 802.3ad
miimon: 100
updelay: 200
downdelay: 200
xmitHashPolicy: layer3+4
lacpRate: slow
adActorSysPrio: 65535
resendIGMP: 1
packetsPerSlave: 1
up: true
addresses:
    - address: 1.2.3.4/24
```

Notes from the page:

- `name` is the bond interface that gets created (`agg.0`); `links` lists the members, and link aliases can be used there.
- This example uses 802.3ad (LACP) with link monitoring through `miimon`, `updelay` and `downdelay`.
- Addresses and routes live in the same document, as in static link configuration; DHCP can be enabled on the bond as in dynamic link configuration.
- MTU is set with `mtu`. The bond inherits the MAC of the first link in `links` unless `hardwareAddr` is set.

The reference page lists further options such as ARP monitoring (`arpInterval`, `arpIpTargets`), `failOverMac`, `adSelect`, `primary` and `primaryReselect`.

## Checked

2026-11-04. BondConfig example, field semantics, MTU and MAC inheritance confirmed on the Bond page; optional fields listed on the BondConfig reference page.

Method: documentation only; no commands were run.
