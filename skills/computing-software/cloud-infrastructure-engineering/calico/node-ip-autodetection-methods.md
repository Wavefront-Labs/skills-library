---
id: computing-software.cloud-infrastructure-engineering.calico.node-ip-autodetection-methods
name: node-ip-autodetection-methods
category: computing-software
field: cloud-infrastructure-engineering
product: calico
tags: [ipam, autodetection, node-address, installation, can-reach, cidrs, interface, multi-nic]
level: practitioner
status: docs-checked
description: "Control the host IP Calico uses for routing: first-found, kubernetes NodeInternalIP, canReach, interface and skipInterface regexes, cidrs; set in Installation or calico-node env."
sources:
  - https://docs.tigera.io/calico/latest/networking/ipam/ip-autodetection
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Each node needs an IPv4 and/or IPv6 address for inter-node routing. At install, a Node resource is created from detected routing information and shows the result under `spec.bgp` (`ipv4Address`, `ipv6Address`, `asNumber`, and the tunnel address such as `ipv4IPIPTunnelAddr`).

The default method is **first-found**: the first valid address on the first valid interface, ignoring local interfaces such as the Docker bridge. Use another method for hosts with multiple external interfaces, multiple addresses on one interface, or changing host IPs.

Operator installs set it in the Installation resource under `spec.calicoNetwork.nodeAddressAutodetectionV4` (use `nodeAddressAutodetectionV6` for IPv6):

| Method | Field and example |
|---|---|
| Kubernetes node IP (first internal IP in `Status.Addresses`) | `kubernetes: NodeInternalIP` |
| Source address used to reach an IP or name | `canReach: 8.8.8.8` |
| Include interfaces by regex | `interface: eth.*` |
| Exclude interfaces by regex | `skipInterface: eth.*` |
| Addresses within CIDRs | `cidrs:` list such as `'192.168.200.0/24'` |

Example:

```yaml
kind: Installation
apiVersion: operator.tigera.io/v1
metadata:
  name: default
spec:
  calicoNetwork:
    nodeAddressAutodetectionV4:
      canReach: 8.8.8.8
```

For manifest installs set the environment variable on the daemon set:

```bash
kubectl set env daemonset/calico-node -n kube-system IP_AUTODETECTION_METHOD=<autodetection-method>
```

with `IP6_AUTODETECTION_METHOD` for IPv6. The node configuration reference defines the method value syntax.

## Checked

2026-11-04. Method list, operator field names, YAML examples and the kubectl set env command were confirmed on the Configure IP autodetection page.

Method: documentation only; no commands were run.
