---
id: computing-software.systems-network-administration.windows-server.asr-network-mapping-and-ip-retention
name: asr-network-mapping-and-ip-retention
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, azure-site-recovery, asr, asr-network-mapping, ip-retention, target-subnet, static-ip-failover, dns-update]
level: advanced
status: docs-checked
description: "Plan ASR networking: VM network mapping, keeping or changing IPs on failover, subnet failover design, test VNet isolation and DNS update strategies."
sources:
  - https://learn.microsoft.com/en-us/azure/site-recovery/concepts-on-premises-to-azure-networking
  - https://learn.microsoft.com/en-us/azure/site-recovery/hyper-v-vmm-network-mapping
  - https://learn.microsoft.com/en-us/azure/site-recovery/site-recovery-retain-ip-azure-vm-failover
  - https://learn.microsoft.com/en-us/azure/site-recovery/site-recovery-test-failover-to-azure
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ASR network mapping and IP retention

## Network mapping
- Hyper-V with VMM: map each source VMM VM network to an Azure virtual network. After failover VMs connect to the
  mapped network; if the target network has a subnet with the same name as the source subnet the replica joins it,
  otherwise it joins the first subnet.
- Without VMM, and for VMware or physical machines: set the target network and subnet per replicated item in
  **Compute and Network**.
- Azure to Azure: target VNet mapping is created or chosen when you enable replication.

## Retain IPs
Set the target network and IP in the replicated item's Compute and Network properties to mirror the source.
- If the target Azure VM uses the same IP address/subnet as on-premises, site-to-site VPN or ExpressRoute between
  them cannot work because the ranges overlap. Azure has no stretched VLANs, so retaining IPs means taking the IP
  space to Azure by failing over the whole subnet and changing routes after failover.
- Azure to Azure: static source IPs are provisioned on the target if the address is available; retaining them
  conflicts with VPN between source and target networks that share an address space. Failing over one app subnet while
  keeping IPs is not generally advisable; isolate each app in its own VNet or use different target IPs.
- DCs/DNS must be reachable from the target VNet (VNet DNS setting).

## Change IPs
Use a different address range in Azure and set the target IP per VM.
- Update DNS with low TTLs or a recovery plan runbook; public names can use Azure Traffic Manager, and a public IP
  can be attached during failover by a script or runbook in a recovery plan (the on-premises public IP cannot be reused).
- Applications with hard-coded IPs need config change scripts in the recovery plan.

## Test failover network
Use a network isolated from the production recovery network (a newly created VNet is isolated by default) that mimics
production: same number of subnets with the same names, same IP address range, no site-to-site connectivity, and
DNS pointing at the IP set for the DNS VM in Compute and Network.

## Checklist
- [ ] Every protected VM has target subnet, IP, NSG, and (if needed) public IP plan.
- [ ] DNS strategy documented and exercised in a test failover.

## Checked
Date 2026-10-27. Documentation: on-premises to Azure networking concepts, Hyper-V (VMM) network mapping, retain IP
addresses (Azure VMs) and test failover pages. Confirmed: subnet-name matching, overlap and stretched-VLAN
limitation, Target IP setting, public IP handling, test network requirements.
Method: documentation only; no commands were run.
