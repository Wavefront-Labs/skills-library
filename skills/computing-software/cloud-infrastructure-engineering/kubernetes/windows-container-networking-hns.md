---
id: computing-software.cloud-infrastructure-engineering.kubernetes.windows-container-networking-hns
name: windows-container-networking-hns
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, windows-nodes, hns, windows-networking, calico, flannel]
level: practitioner
status: docs-checked
description: "Understand Windows container networking on Kubernetes (HNS networks, endpoints and load-balancer policies, Calico and Flannel modes, kube-proxy kernelspace) and debug it."
sources: ["https://kubernetes.io/docs/concepts/services-networking/windows-networking/", "https://kubernetes.io/docs/tasks/debug/debug-cluster/windows/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Windows container networking (HNS)

On Windows nodes, networking for containers is exposed through CNI plugins. Each container has a vNIC attached to a Hyper-V virtual switch. The Host Compute Service (HCS) manages containers; the Host Networking Service (HNS) manages virtual networks (including vSwitches), endpoints and vNICs, namespaces, and policies (encapsulation, load-balancing rules, ACLs, NAT). DNS, routes and metrics live in the container's own registry rather than in files, so CNI implementations must call HNS instead of mapping files into the container.

## Network modes and plugins (Kubernetes docs)
| Mode | Plugins named in the docs | Notes |
|---|---|---|
| L2bridge | win-bridge, Azure-CNI, Flannel host-gateway (uses win-bridge) | Containers sit on the underlay; needs user-defined routes between nodes |
| L2Tunnel | Azure-CNI | Special case of l2bridge, Azure only |
| Overlay (Beta) | win-overlay, Flannel VXLAN (uses win-overlay) | VXLAN encapsulation; isolates container networks from the host underlay |
| Transparent | ovn-kubernetes | Special use case |
| NAT | nat | Not used in Kubernetes |

Flannel host-gateway has stable support on Windows; Flannel VXLAN is Beta. Flannel on Windows is restricted to VNI 4096 and UDP port 4789. For other CNIs (for example Calico) read that project's Windows documentation for supported modes and policy features.

IPAM options on Windows: host-local, azure-vnet-ipam (azure-cni only), and Windows Server IPAM as the fallback when none is set.

## Services
Supported Service types: NodePort, ClusterIP, LoadBalancer, ExternalName. Settings:
| Feature | Minimum Windows build | How to enable |
|---|---|---|
| Session affinity | Windows Server 2022 | `service.spec.sessionAffinity: ClientIP` |
| Direct Server Return (DSR) | Windows Server 2019 | kube-proxy `--enable-dsr=true` (`WinDSR` feature gate: beta 1.33, stable 1.34) |
| Preserve-Destination | Windows Server, version 1903 | service annotation `"preserve-destination": "true"` plus DSR in kube-proxy |
| Client IP preservation | Windows Server 2019 | `externalTrafficPolicy: Local` plus DSR in kube-proxy |

## Not supported
- Host networking mode.
- Local NodePort access from the node itself (works from other nodes and external clients). Windows hosts also cannot reach the IP of Services scheduled on them; Windows Pods can.
- More than 64 backend Pods (unique destination addresses) per Service.
- IPv6 between Windows Pods on overlay networks; Local traffic policy without DSR.
- Outbound ICMP through win-overlay, win-bridge or Azure-CNI to a remote network (ping to the internet fails; use `curl`). TCP/UDP work.

## Troubleshooting (Kubernetes Windows debugging tips)
- Pods have no connectivity when nodes are VMs: enable MAC spoofing on all VM network adapters.
- vNICs and HNS endpoints are deleted: kube-proxy was started without `--hostname-override`; pass the node hostname.
- No network adapter when the kubelet starts: in an admin shell, `Get-HnsNetwork | ? Name -ieq "cbr0"` and `Get-NetAdapter | ? Name -Like "vEthernet (Ethernet*"` return nothing when virtual network creation failed.
- Outbound traffic not SNAT-ed with l2bridge: the external IP must not be in the CNI `ExceptionList` (cluster, service and management subnets belong there).
- Flannel node rejoin: remove the old `SourceVip.json` and `SourceVipRequest.json` files from the node's Kubernetes directory before rejoining.
- `kubectl port-forward` fails with "wincat not found": use a pause image that includes `wincat.exe` (the maintained pause image does).

## Verify
A Windows Pod resolves and reaches a Linux Service and a Linux Pod by IP; remember ping to outside networks is expected to fail.

## Checked

Checked 2026-10-26 against Kubernetes website docs (main branch, latest commit 2026-10-25, covering Kubernetes 1.36). Confirmed: network modes and plugins, Service settings and minimum Windows builds, WinDSR gate stages, unsupported networking features, debugging tips.

Method: documentation only; no commands were run.
