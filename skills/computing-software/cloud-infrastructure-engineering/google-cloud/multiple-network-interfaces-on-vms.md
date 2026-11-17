---
id: computing-software.cloud-infrastructure-engineering.google-cloud.multiple-network-interfaces-on-vms
name: multiple-network-interfaces-on-vms
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, vpc, multi-nic, multiple-network-interfaces, network-virtual-appliance, policy-routing, ilb-next-hop]
level: practitioner
status: docs-checked
description: "Create multi-NIC Compute Engine VMs for network appliances: one NIC per VPC, NIC limits by vCPU, guest policy routing, and next-hop internal load balancers for HA appliances."
sources: ["https://cloud.google.com/vpc/docs/multiple-interfaces-concepts", "https://cloud.google.com/vpc/docs/create-use-multiple-interfaces", "https://cloud.google.com/load-balancing/docs/internal/ilb-next-hop-overview"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Multiple network interfaces on VMs

## Rules
- Each network interface must use a unique subnet. Two or more vNICs can share a VPC network only if that network also contains `nic0`.
- The vNIC count scales with vCPUs, up to 10 for most machine types; bare metal and accelerator-optimized types have their own limits (see the maximum-interfaces table). Dynamic NICs (VLAN interfaces named like `nic0.4`, VLAN ID 2 to 255) allow up to 16 interfaces in total and can be added to or removed from existing instances.
- The default route comes from DHCP and is associated with `nic0`; traffic to connected subnets leaves via `nic0` unless you configure routing otherwise.

## Create
```bash
gcloud compute instances create fw-1 --zone=<Z> --machine-type=n2-standard-4 --can-ip-forward \
  --network-interface=network=untrust,subnet=untrust-ew2,no-address \
  --network-interface=network=trust,subnet=trust-ew2,no-address \
  --network-interface=network=mgmt,subnet=mgmt-ew2,no-address
```
IP forwarding is a per-instance setting that applies to all interfaces; enable it (`--can-ip-forward`) for
appliances that route packets. The `constraints/compute.vmCanIpForward` org policy constraint can restrict it.

## Guest policy routing (Linux)
Traffic arriving on nic1 must leave via nic1:
```bash
echo "1 rt1" | sudo tee -a /etc/iproute2/rt_tables
sudo ip route add 10.20.0.0/24 dev ens5 table rt1
sudo ip route add default via 10.20.0.1 dev ens5 table rt1
sudo ip rule add from 10.20.0.5/32 table rt1
```
The interface name (`ens5`) and addresses are examples; use your guest's interface names.

## HA appliances
Put two or more appliances behind an **internal passthrough Network Load Balancer** (it operates within a single VPC network, so use one per NIC network; one sends packets to `nic0` of the backends and another to `nic1`) and use it as the next hop of a static route.
The load balancer's health check keeps new connections on healthy appliances.

## Gotchas
- Firewall rules apply per network; each NIC's VPC needs its own rules.
- Adding or removing vNICs on an existing instance is done with Dynamic NICs, which need extra guest setup.

## Verify
- [ ] `ip addr` shows all NICs; traffic from trust to internet flows through the appliance.

## Checked

Checked 2026-10-27 against About multiple network interfaces, Create VMs with multiple network interfaces, the internal passthrough Network Load Balancer next-hop page and the organization policy constraints list. Fixed wrong claims: NICs may share a VPC if it also holds nic0, each NIC needs a unique subnet, the vNIC maximum scales with vCPUs up to 10 for most machine types (16 interfaces with Dynamic NICs), and existing instances change interfaces through Dynamic NICs. Confirmed the nic0 default route, per-instance IP forwarding, --network-interface syntax and the ILB next-hop behaviour. Removed the subnet-overlap and guest-environment claims.

Method: documentation only; no commands were run.
