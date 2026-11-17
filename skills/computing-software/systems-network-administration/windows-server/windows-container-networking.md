---
id: computing-software.systems-network-administration.windows-server.windows-container-networking
name: windows-container-networking
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, windows-containers, container-nat-network, l2bridge, transparent-network, overlay, hns, docker-network-create, port-publishing, get-hnsnetwork]
level: practitioner
status: docs-checked
description: "Windows container network drivers: NAT (default) with port publishing, transparent and l2bridge for routable IPs, overlay for swarm/k8s, and HNS troubleshooting."
sources:
  - https://learn.microsoft.com/en-us/virtualization/windowscontainers/container-networking/network-drivers-topologies
  - https://learn.microsoft.com/en-us/virtualization/windowscontainers/container-networking/advanced
  - https://learn.microsoft.com/en-us/virtualization/windowscontainers/container-networking/architecture
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Windows container networking
Networks are implemented by the Host Networking Service (HNS) and a Hyper-V virtual switch. Create custom networks with
`docker network create -d <driver> <name>`.

| Driver | Behaviour (documented) | Typical use |
|---|---|---|
| **nat** (default) | internal Hyper-V switch; IPs from the `--subnet` prefix; port forwarding from host to container supported; cross-subnet container traffic not supported (one NAT prefix) | developers, single host |
| **transparent** | external Hyper-V switch, directly on the physical network; static IPs (needs `--subnet`) or an external DHCP server; MAC address spoofing is required when the host is a VM; not supported on Azure VMs | small deployments |
| **overlay** | VXLAN across hosts, each network with its own subnet; used by Docker Swarm, available in Kubernetes; may need specific KBs on older Windows Server versions | multi-node |
| **l2bridge** | external switch, container traffic uses the host MAC through MAC re-write; subnet same as the host or a new custom subnet | Kubernetes and Microsoft SDN |
| **l2tunnel** | like l2bridge but all traffic goes to the virtualization host for SDN policy; only for Microsoft cloud stacks (Azure) | Azure |

## Examples
```powershell
docker network create -d nat --subnet 10.244.0.0/24 my_nat
docker network create -d transparent --subnet 10.244.0.0/24 --gateway 10.244.0.1 -o com.docker.network.windowsshim.vlanid=7 -o com.docker.network.windowsshim.dnsservers="10.244.0.7" my_transparent
docker network create -d l2bridge --subnet 10.244.0.0/24 --gateway 10.244.0.1 my_l2bridge
docker network create -d transparent -o com.docker.network.windowsshim.interface="Ethernet 2" TeamedNet   # pick the host adapter
docker network ls ; docker network inspect nat
```
- The default `nat` subnet can be customised with the `fixed-cidr` setting in the Docker daemon configuration file.
- NAT networks created on Windows Server 2019 and later are not persisted across reboots.
- On overlay networks on Windows Server 2019 and later, outbound connectivity uses VFP NAT rules, so use TCP/UDP options
  rather than ICMP in `ping` or `Test-NetConnection` while debugging.

## Verify
- [ ] The container gets an address from the intended network (`docker network inspect`).
- [ ] A published port on a nat network is reachable from another machine.

## Checked

2026-10-26 against the Windows containers docs (container network drivers and topologies, advanced container networking; Virtualization-Documentation last commit 2026-10-20): driver behaviours and requirements, fixed-cidr tip, NAT persistence note, docker network create examples including the windowsshim vlanid, dnsservers and interface options, overlay VFP NAT note. Removed unconfirmed claims about 172.x NAT addressing, flannel modes, the `--ip` example, the Get-HnsNetwork and Get-NetNat troubleshooting block, the localhost caveat, the cleanup-scripts claim and the DNS inheritance remark.

Method: documentation only; no commands were run.
