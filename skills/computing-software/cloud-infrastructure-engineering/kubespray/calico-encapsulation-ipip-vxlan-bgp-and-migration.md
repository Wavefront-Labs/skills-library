---
id: computing-software.cloud-infrastructure-engineering.kubespray.calico-encapsulation-ipip-vxlan-bgp-and-migration
name: calico-encapsulation-ipip-vxlan-bgp-and-migration
category: computing-software
field: cloud-infrastructure-engineering
product: kubespray
tags: [calico, vxlan, ipip, bgp, encapsulation, calicoctl, migration]
level: advanced
status: docs-checked
description: "Select Calico encapsulation in Kubespray (VXLAN, IP in IP, plain BGP) and migrate from IP in IP to VXLAN before upgrading past 2.18."
sources:
  - https://kubespray.io/docs/CNI/calico.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
IP in IP and VXLAN are mutually exclusive. VXLAN is the more mature implementation and enabled by default. Kubespray defaults changed after v2.18 from auto-enabling `ipip` to auto-enabling `vxlan`. If you run default Calico settings and upgrade to 2.19 or later, either migrate to VXLAN manually first or pin the pre-2.19 settings.

**IP in IP** (requires the bird backend):

```yml
calico_ipip_mode: 'Always'  # Possible values is `Always`, `CrossSubnet`, `Never`
calico_vxlan_mode: 'Never'
calico_network_backend: 'bird'
```

**BGP without encapsulation**:

```yml
calico_ipip_mode: 'Never'
calico_vxlan_mode: 'Never'
calico_network_backend: 'bird'
```

**Migration** to VXLAN must happen before upgrading; `cluster.yml` and `upgrade-cluster.yml` refuse to continue on incompatible settings. On a control plane node, with a healthy cluster:

```shell
calicoctl.sh patch felixconfig default -p '{"spec":{"vxlanEnabled":true}}'
calicoctl.sh patch ippool default-pool -p '{"spec":{"ipipMode":"Never", "vxlanMode":"Always"}}'
```

Wait until the `vxlan.calico` interfaces exist on all nodes and traffic flows through them, then:

```shell
calicoctl.sh patch felixconfig default -p '{"spec":{"ipipEnabled":false}}'
```

Playbooks only handle the default pool created by Kubespray, so patch any other pools yourself. For IPv6 VXLAN the kernel must be 3.12 or newer, otherwise do not set `calico_vxlan_mode_ipv6: Always`.

## Checked

2026-11-08. Cited pages re-read in full. Modes, migration commands and warnings were confirmed under Config encapsulation for cross server traffic on the Calico page.

Method: documentation only; no commands were run.
