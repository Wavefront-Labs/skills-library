---
id: computing-software.cloud-infrastructure-engineering.talos-linux.layer2-vip-control-plane
name: layer2-vip-control-plane
category: computing-software
field: cloud-infrastructure-engineering
product: talos-linux
tags: [vip, layer2vipconfig, control-plane, etcd-election, high-availability, kubernetes-api]
level: practitioner
status: docs-checked
description: "Give the Kubernetes API a floating virtual IP with Layer2VIPConfig: L2 requirement, etcd election, failover timing, and why the VIP must not be the talosconfig endpoint."
sources:
  - https://github.com/siderolabs/docs/blob/main/public/talos/v1.15/networking/advanced/vip.mdx
  - https://github.com/siderolabs/docs/blob/main/public/talos/v1.15/reference/configuration/network/layer2vipconfig.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Talos can float a shared virtual IP across control plane nodes with no load balancer. The control plane machines compete for the address through etcd elections, and only one owns it at a time.

Requirements:

- Control plane nodes must share a layer 2 network (a switch, no router between them) and the VIP comes from that subnet.
- Pick a reserved address the DHCP server cannot hand out. Example nodes `192.168.0.10`, `.11`, `.12`; VIP `192.168.0.15`.
- Control plane only; any other use is unsupported. The address is announced with gratuitous ARP for IPv4.

Patch every control plane node with a `Layer2VIPConfig` document (it can also sit on a logical link such as a VLAN):

```yaml
apiVersion: v1alpha1
kind: Layer2VIPConfig
name: 192.168.0.15
link: enp0s2
```

Caveats:

- Elections need etcd, so the VIP only comes up after Kubernetes is bootstrapped.
- Do not use the VIP as the `endpoint` in `talosconfig`: it depends on etcd and kube-apiserver health, so you could not use the Talos API to repair either one.
- Reaching the Talos API through the VIP works but is not recommended, for the same reason.

Failover: a graceful shutdown moves the VIP almost instantly. A crash or power loss takes up to about a minute, by design, because the election timeout prevents two nodes believing they own the VIP (split brain). Only external clients feel it; in-cluster pods keep reaching the API through KubePrism and discovery. Long-lived HTTP/2 connections may break and should reconnect.

## Checked

2026-11-04. Requirements, Layer2VIPConfig YAML, caveats and failover behaviour confirmed on the Virtual (shared) IP page; document purpose (gratuitous ARP, control plane only) confirmed on the Layer2VIPConfig reference page.

Method: documentation only; no commands were run.
