---
id: computing-software.cloud-infrastructure-engineering.kubespray.calico-wireguard-mtu-and-tuning-options
name: calico-wireguard-mtu-and-tuning-options
category: computing-software
field: cloud-infrastructure-engineering
product: kubespray
tags: [calico, wireguard, mtu, felix, probes, ipam, rpf]
level: advanced
status: docs-checked
description: "Enable Calico WireGuard in Kubespray, compute calico_veth_mtu, and apply smaller options: host action, probes, host-local IPAM, RPF."
sources:
  - https://kubespray.io/docs/CNI/calico.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
**WireGuard.** Set `calico_wireguard_enabled: true`. CentOS 8, AlmaLinux 8, Rocky Linux 8 and Amazon Linux 2 also need `epel_enabled: true` to get the wireguard tools.

**MTU.** Usually leave `calico_veth_mtu` alone; Calico calculates it. If you must set it, subtract from the network MTU: 60 with WireGuard (1440 on 1500), 50 with VXLAN or BPF mode (1450), 20 with IPIP (1480), nothing with no encapsulation.

```yaml
calico_veth_mtu: 1440
```

**Other options documented:**
- `calico_endpoint_to_host_action: "ACCEPT"`: Calico drops endpoint-to-host traffic by default; Kubespray defaults to RETURN, otherwise pods to hostNetwork services on the same node are dropped.
- `calico_healthhost: "0.0.0.0"`: Felix health listens on localhost only since Calico 3.2.0.
- `calico_node_livenessprobe_timeout: 10` and `calico_node_readinessprobe_timeout: 10`.
- `nat_outgoing_ipv6: true` for outgoing IPv6 from pods (default false).
- `calico_ipam_host_local: true` to use the host-local IPAM from `Node.podCIDR` instead of calico-ipam.
- `calico_node_ignorelooserpf: true` because Felix aborts if the kernel RPF is not strict.
- `calico_feature_detect_override: "ChecksumOffloadBroken=false"` to enable VXLAN offload (may break on buggy NIC drivers).
- `calico_node_extra_envs`, e.g. `FELIX_DEVICEROUTESOURCEADDRESS`.
- `calico_cni_log_file_path: false` disables CNI logging to disk.

On OpenStack, allow `ipip` traffic in security groups or you will see timeouts.

## Checked

2026-11-08. Cited pages re-read in full. Each variable and the MTU arithmetic were confirmed on the Calico page.

Method: documentation only; no commands were run.
