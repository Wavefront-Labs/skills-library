---
id: computing-software.cloud-infrastructure-engineering.azure.load-balancer-inbound-nat-rules
name: load-balancer-inbound-nat-rules
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, load-balancer, inbound-nat-rules, nat-rules, port-forwarding, vmss, frontend-port-range]
level: practitioner
status: docs-checked
description: "Configure Standard Load Balancer inbound NAT rules for per-instance port forwarding: single-VM rules, backend-pool port ranges for VMSS, and safer admin-port alternatives."
sources: ["https://learn.microsoft.com/azure/load-balancer/inbound-nat-rules", "https://learn.microsoft.com/azure/load-balancer/manage-inbound-nat-rules", "https://learn.microsoft.com/en-us/cli/azure/network/lb/inbound-nat-rule", "https://learn.microsoft.com/en-us/cli/azure/network/lb"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Load Balancer inbound NAT rules

**Goal:** reach a specific backend instance on a specific port through the load balancer frontend (port forwarding), without
a public IP on each VM. Unlike load-balancing rules, NAT rules do not need a health probe.

## V2 rule (backend pool): recommended for multiple VMs and scale sets
```bash
az network lb inbound-nat-rule create --resource-group myResourceGroup --lb-name myLoadBalancer --name myInboundNATrule \
  --protocol Tcp --backend-pool-name myBackendPool --frontend-ip-name myFrontend \
  --frontend-port-range-start 500 --frontend-port-range-end 1000 --backend-port 443
az network lb list-mapping -n myLoadBalancer -g myResourceGroup --backend-pool-name myBackendPool --request ip=<backend-ip>
```
- A frontend port range is preallocated from the range start and the "maximum number of machines in the backend pool"
  (the page: range 500-1000 limits the pool to 500 VMs). Each backend machine gets a mapping from that range.
- Scale-down keeps the mappings of the remaining VMs; scale-up creates new mappings automatically.
- If the range runs out of free ports, scaling up the pool is blocked, which can leave new instances without connectivity.
  Widen the range with `az network lb inbound-nat-rule update ... --frontend-port-range-end 1500` (page: raises the cap to 1,000 machines from 500).
- View mappings in the portal (rule properties, Port mapping section) or with `list-mapping` (`--request ip=...` or `nic=...`).

## V1 rule: single VM, 1:1 mapping
```bash
az network lb inbound-nat-rule create --backend-port 443 --lb-name myLoadBalancer --name myInboundNATrule \
  --protocol Tcp --resource-group myResourceGroup --frontend-ip-name myFrontend --frontend-port 500
az network nic ip-config inbound-nat-rule add --resource-group myResourceGroup --nic-name MyNic \
  --ip-config-name MyIpConfig --inbound-nat-rule myInboundNATrule --lb-name myLoadBalancer
```
Inbound NAT pools (the scale-set form of V1 rules) retire on 30 September 2027, and from 15 November 2026 you cannot create new
ones: move to V2 rules. Single-VM V1 rules are not affected.

## Options (CLI reference)
- `--floating-ip true`: the reference describes it as the setting required for SQL Always On availability groups; it cannot be changed after the endpoint is created.
- `--idle-timeout` (minutes): the reference says 4 to 30, default 4, TCP only. `--enable-tcp-reset` sends a bidirectional TCP reset on idle timeout or unexpected termination.
- Frontend ports (and range ends) accept 1 to 65534; frontend port numbers must be unique across rules in the load balancer.

## Security
Forwarding 22 or 3389 on a public frontend exposes admin ports. Prefer Azure Bastion, or an internal frontend reached over VPN or
ExpressRoute, and restrict sources in the backend NSG.

## Verify
- [ ] `az network lb list-mapping` shows each backend IP with its frontend port.
- [ ] A client connects to `<frontend-ip>:<frontend-port>` and reaches the intended instance's backend port.

## Checked

2026-11-07. Re-read in full: Inbound NAT rules, Manage inbound NAT rules (portal/PowerShell/CLI tabs, which are in the text). In the CLI references for `az network lb inbound-nat-rule` and `az network lb` I read the flag lists and parameter descriptions for create/update and `list-mapping`, not every other command.
- Corrected: idle timeout was "4-100 minutes"; the CLI reference says 4 to 30 minutes (default 4). Flag `--frontend-ip` kept out of examples in favour of `--frontend-ip-name`, the form on the manage page.
- Removed: "Each instance gets the next frontend port" wording, floating IP "when the backend binds the frontend IP", the claim that NAT rules have no source filter, the "removed instance frees its port / re-add may differ" gotcha (page says remaining mappings persist on scale-down), the outbound-NAT remark, `nc -vz` Verify step.
- Dropped from `sources`: the virtual machine scale set networking article (not about NAT rules beyond a passing mention); added the two CLI reference pages actually used.

Method: documentation only; no commands were run.
