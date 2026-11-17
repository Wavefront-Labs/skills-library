---
id: computing-software.systems-network-administration.virtualisation.hyper-v-sdn-network-controller
name: hyper-v-sdn-network-controller
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [network-controller-sdn, sdn, hyper-v, vxlan, software-load-balancer]
level: advanced
status: docs-checked
description: "Deploy and operate the Windows Server SDN Network Controller for Hyper-V: SDN Express or WAC deployment, virtual networks over VXLAN, SLB and gateways, health checks."
sources:
  - https://learn.microsoft.com/en-us/windows-server/networking/sdn/technologies/network-controller/network-controller-failover-clustering
  - https://learn.microsoft.com/en-us/windows-server/networking/sdn/technologies/network-controller/network-controller-service-fabric
  - https://learn.microsoft.com/en-us/azure/azure-local/concepts/plan-software-defined-networking-infrastructure-23h2
  - https://learn.microsoft.com/en-us/windows-server/networking/sdn/deploy/deploy-a-software-defined-network-infrastructure-using-scripts
  - https://learn.microsoft.com/en-us/windows-server/networking/sdn/manage/create-a-tenant-vm
  - https://github.com/microsoft/SDN
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SDN Network Controller

**Goal:** centrally managed virtual networks, ACLs and load balancing for Hyper-V, decoupled from physical VLANs.

## Components
- **Network Controller (NC)**: REST API and policy store (a Service Fabric application on NC servers or VMs, or, from Windows Server 2025 and Azure Local 2311.2, a Failover Clustering service deployed on the hosts).
- **Hyper-V hosts** running the SDN Host Agent, which programs network policy.
- **Software Load Balancer (SLB) MUX** VMs for VIPs and outbound NAT (BGP to the top-of-rack routers).
- **RAS Gateways** connecting virtual networks to external networks (BGP peering as for the SLB).
- **HNV Provider network** (provider addresses): the physical network for East/West and North/South tenant traffic and for BGP peering with the physical network.

## Deploy
- SDN Express: `SDNExpress.ps1 -ConfigurationDataFile FabricConfig.psd1` from the SDNExpress folder (microsoft/SDN GitHub repo), then `SDNExpressTenant.ps1` with `TenantConfig.psd1` for a sample tenant workload; Windows Admin Center, VMM and the Azure portal (Azure Local) are the other documented deployment routes.
- Requirements from the planning page: switchport MTU of at least 1674 bytes (including the L2 Ethernet header) on the provider network, and BGP (RFC 4271 based ECMP) peering for the SLB/MUX and gateways. A Service Fabric based NC runs on Windows Server Datacenter edition.

## Operating
```powershell
$uri = 'https://nc.example.com'
Get-NetworkControllerVirtualNetwork -ConnectionUri $uri
Get-NetworkControllerNetworkInterface -ConnectionUri $uri | Select ResourceId, @{n='State';e={$_.Properties.ConfigurationState.Status}}
Get-NetworkControllerServer -ConnectionUri $uri          # host registration and health
Debug-NetworkController -NetworkController nc.example.com   # queries the NC for detailed diagnostics (needs the NC REST certificate and L3 access to the REST IP)
Debug-NetworkControllerConfigurationState -NetworkController nc.example.com
```
WAC exposes virtual networks, logical networks, ACLs and SLB for day-to-day work.

## VM attachment
A VM NIC joins a virtual network by being created as an NC network interface and having that interface's `InstanceId` set as the profile ID on the Hyper-V port (Microsoft's Create a Tenant VM page shows the steps; SCVMM can also do it). The VM adapter needs a static MAC address for the VM's lifetime, and the VM should not start before the interface ID is set.

## Gotchas
- A provider-network MTU below the documented 1674-byte minimum is the usual cause of large-packet loss inside virtual networks.

## Verify
`Debug-NetworkControllerConfigurationState` reports no errors; VMs in a virtual network reach each other across hosts; `Get-ProviderAddress` on hosts shows the provider addresses.

## Checked

Checked 2026-10-26 against MicrosoftDocs/windowsserverdocs (Network Controller with Failover Clustering and with Service Fabric, SDN Express deployment, Create a Tenant VM; latest commit 2026-10-23) and the Azure Local SDN planning page (MicrosoftDocs/azure-stack-docs). Confirmed: NC on Failover Clustering from Windows Server 2025 and Azure Local 2311.2, the 1674-byte minimum MTU, BGP requirements, SDN Express script names, static MAC and InstanceId port profile steps, and the NetworkController, NetworkControllerDiagnostics and HNVDiagnostics cmdlets. Removed as undocumented or wrong: VXLAN and VFP statements (the docs say host agent and HNV provider network), the AD and certificate requirements list, the certificate-expiry and mixed-port gotchas, and the `ConfigurationState: Success` check.

Method: documentation only; no commands were run.
