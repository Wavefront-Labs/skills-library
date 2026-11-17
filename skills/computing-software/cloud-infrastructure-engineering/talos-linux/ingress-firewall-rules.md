---
id: computing-software.cloud-infrastructure-engineering.talos-linux.ingress-firewall-rules
name: ingress-firewall-rules
category: computing-software
field: cloud-infrastructure-engineering
product: talos-linux
tags: [firewall, ingress, networkrule, nftables, networkdefaultaction, security]
level: advanced
status: docs-checked
description: "Restrict host service access with NetworkDefaultActionConfig and NetworkRuleConfig: block mode, allowed interfaces, port ranges, control plane and worker rules, CNI VXLAN ports."
sources:
  - https://github.com/siderolabs/docs/blob/main/public/talos/v1.15/networking/ingress-firewall.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The ingress firewall limits access to host services (apid, kubelet and any host-network workload). It does not filter pod-to-pod traffic; use CNI network policies for that. A node-level tool such as Cilium Host Firewall may take precedence in the nftables chain.

Two document kinds: one `NetworkDefaultActionConfig` (`ingress: accept` default, or `block`) and any number of uniquely named `NetworkRuleConfig` documents:

```yaml
apiVersion: v1alpha1
kind: NetworkDefaultActionConfig
ingress: block
---
apiVersion: v1alpha1
kind: NetworkRuleConfig
name: kubelet-ingress
portSelector:
  ports:
    - 10250
  protocol: tcp
ingress:
  - subnet: 172.20.0.0/24
    except: 172.20.0.1/32
```

Details:

- Traffic on `lo`, `siderolink` and `kubespan` is always allowed. In `block` mode, ICMP/ICMPv6 is allowed at 5 packets per second.
- `ports` takes single ports or ranges like `10300-10400`; `protocol` is `tcp` or `udp`; `except` carves addresses out of a subnet.
- In block mode encapsulated CNI traffic is blocked too: allow Flannel/Calico `vxlan` UDP 4789 or Cilium UDP 8472.
- Recommended control plane set: apid 50000 and Kubernetes API 6443 open, kubelet 10250 and trustd 50001 to the cluster subnet, etcd `2379-2380` to the control plane IPs only. Workers: kubelet and apid to the cluster subnet.
- A mistake can lock you out of the Talos API; apply with `--mode=try` so it reverts.
- Inspect with `talosctl get nftableschain -o yaml`.

## Checked

2026-11-04. Document kinds, always-allowed interfaces, recommended control plane and worker rules, try-mode warning and nftables inspection confirmed on the Ingress Firewall page.

Method: documentation only; no commands were run.
