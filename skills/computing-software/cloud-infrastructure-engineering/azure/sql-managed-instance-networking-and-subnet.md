---
id: computing-software.cloud-infrastructure-engineering.azure.sql-managed-instance-networking-and-subnet
name: sql-managed-instance-networking-and-subnet
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, azure-sql, sql-managed-instance, mi-subnet, mi-networking, subnet-delegation, service-aided-subnet-configuration, public-endpoint, private-endpoint, redirect-connection, network-intent-policy, sql-mi-sizing]
level: advanced
status: docs-checked
description: "Plan and build the SQL Managed Instance subnet: sizing, delegation, service-aided NSG/UDR, public endpoint 3342, private endpoints, redirect vs proxy and cross-VNet access."
sources: ["https://learn.microsoft.com/en-us/azure/azure-sql/managed-instance/connectivity-architecture-overview", "https://learn.microsoft.com/en-us/azure/azure-sql/managed-instance/vnet-subnet-determine-size", "https://learn.microsoft.com/en-us/azure/azure-sql/managed-instance/public-endpoint-configure", "https://learn.microsoft.com/en-us/azure/azure-sql/managed-instance/private-endpoint-overview"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SQL Managed Instance networking and subnet

**Goal:** a dedicated MI subnet sized for growth and upgrades, connectivity from apps,
on-prem and other VNets that works first time, and no surprise when you scale or add instances.

## 1. Subnet design
- **Dedicated subnet**, delegated to `Microsoft.Sql/managedInstances`; nothing else may live in it.
  Multiple MIs can share it (instance pools or separate instances) if sized for all.
- **Size**: each managed instance needs a minimum of 32 IP addresses, so the smallest subnet mask is **/27**. The sizing article
  counts addresses used by Azure (shared by all instances in the subnet), per-instance addresses (General Purpose uses two, Business Critical five),
  and each scaling request temporarily doubles the instance's allocation. Use its table to size the subnet for every instance you plan.
- **Service-aided subnet configuration**: delegation makes Azure apply a network intent
  policy that owns required NSG rules and routes (`Microsoft.Sql-managedInstances_UseOnly_*`).
  Attach your own NSG and route table, but don't delete the platform-added entries.
```bash
az network vnet subnet create -g rg-data --vnet-name vnet-data -n snet-sqlmi --address-prefixes 10.20.4.0/24 \
  --delegations Microsoft.Sql/managedInstances --network-security-group nsg-sqlmi --route-table rt-sqlmi
az sql mi create -g rg-data -n sqlmi-prod --subnet <snet-sqlmi-id> --capacity 8 --edition GeneralPurpose --family Gen5 \
  --storage 512 --license-type BasePrice --minimal-tls-version 1.2 --zone-redundant true --admin-user <user> --admin-password <pwd>
```

## 2. Connectivity options
| Path | How |
|---|---|
| Same/peered VNet, on-prem via VPN/ER | VNet-local endpoint `<mi>.<dns-zone>.database.windows.net`, port 1433 |
| Redirect / Proxy | connection types described in the connectivity architecture article; the Proxy type goes through the gateway on 1433 |
| **Public endpoint** | `<mi>.public.<dns-zone>.database.windows.net` **port 3342**, enable with `az sql mi update --public-data-endpoint-enabled true`, then restrict the NSG to the sources you need |
| **Private endpoint** | from other VNets/tenants without peering, port 1433 (see the private endpoint overview) |
- Outbound from MI (linked servers, DB Mail, backup to URL) follows your UDRs — route via firewall and allow destinations.

## Gotchas
- Failover groups need the two MI subnets non-overlapping and ports 5022 and 11000–11999 open between them.

## Verify
- [ ] `az network vnet subnet show ... --query "delegations[0].serviceName"` is `Microsoft.Sql/managedInstances` and free IPs exceed one extra instance's footprint.
- [ ] From an app VM: `Test-NetConnection <mi-fqdn> -Port 1433` succeeds.
- [ ] Public endpoint either disabled or NSG restricted to named sources on 3342.

## Checked
2026-10-27. Confirmed on Microsoft Learn: vnet-subnet-determine-size (32 IP minimum, /27, General Purpose two and Business Critical five addresses, scaling doubles, Azure-used addresses),
connectivity-architecture-overview (delegation to Microsoft.Sql/managedInstances, network intent policy `UseOnly` rules, Proxy, port 3342), public-endpoint-configure (3342, public FQDN,
--public-data-endpoint-enabled), private-endpoint-overview, failover-group-configure-sql-mi (ports 5022 and 11000-11999), CLI reference for `az sql mi create` (flags in the example).
Removed: /26 and /24 production advice, resize claim, multi-hour first-instance build time, 11000-11999 redirect description and the "default" claim, random DNS suffix statement,
Sept 2020 peering note, NVA/SNAT claim, subnet-move claim, `fullyQualifiedDomainName` query.

Method: documentation only; no commands were run.
