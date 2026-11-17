---
id: computing-software.cloud-infrastructure-engineering.kubespray.flannel-backends-and-verification
name: flannel-backends-and-verification
category: computing-software
field: cloud-infrastructure-engineering
product: kubespray
tags: [flannel, cni, vxlan, host-gw, wireguard, verification]
level: practitioner
status: docs-checked
description: "Use Flannel with its vxlan, host-gw or wireguard backends, apply the VXLAN offload workaround and verify the install from subnet.env, the flannel.1 interface and a test pod."
sources:
  - https://kubespray.io/docs/CNI/flannel.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Flannel is a network fabric for containers, designed for Kubernetes. Kubespray supports the backends `vxlan`, `host-gw` and `wireguard`.

Warning: the `vxlan` backend can hit a known Flannel bug. While waiting on a newer Flannel version, the workaround used in Kubespray's own network test is:

```
ethtool --offload flannel.1 rx off tx off
```

**Verify the install.**
1. The configuration file should exist at `/run/flannel/subnet.env`. The page's sample shows `FLANNEL_NETWORK=10.233.0.0/18`, `FLANNEL_SUBNET=10.233.16.1/24`, `FLANNEL_MTU=1450` and `FLANNEL_IPMASQ=false`.
2. Check that the interface exists with `ip a show dev flannel.1`; the sample shows MTU 1450.
3. Run a container and check its IP:

```ShellSession
kubectl run test --image=busybox --command -- tail -f /dev/null
kubectl describe po test-34ozs | grep ^IP
kubectl exec test-34ozs -- ip a show dev eth0
```

## Checked

2026-11-04. Backends, the workaround and the three verification steps were confirmed on the Flannel page. Removed an MTU remark the Flannel page does not make.

Method: documentation only; no commands were run.
