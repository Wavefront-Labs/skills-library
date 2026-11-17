---
id: computing-software.database-administration.sql-server.azure-sql-firewall-and-private-endpoints
name: azure-sql-firewall-and-private-endpoints
category: computing-software
field: database-administration
product: sql-server
tags: [database-administration, sql-server, azure-sql, azure-sql-firewall, private-endpoint, private-link, public-network-access, sp-set-firewall-rule, vnet-service-endpoint]
level: practitioner
status: docs-checked
description: "Lock down Azure SQL Database network access: server and database firewall rules, private endpoints with private DNS, disabling public access, and testing connectivity."
sources:
  - https://learn.microsoft.com/en-us/azure/azure-sql/database/firewall-configure
  - https://learn.microsoft.com/en-us/azure/azure-sql/database/private-endpoint-overview
  - https://learn.microsoft.com/en-us/azure/azure-sql/database/connectivity-settings
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Azure SQL firewall rules and private endpoints

## Order of evaluation
Connection arrives at the gateway -> database-level IP rules are checked first, then
server-level IP rules.

## Server-level IP rules
```bash
az sql server firewall-rule create -g <rg> -s <server> -n office --start-ip-address 203.0.113.10 --end-ip-address 203.0.113.10
az sql server firewall-rule list -g <rg> -s <server> -o table
```
T-SQL in `master`: `EXEC sp_set_firewall_rule N'office', '203.0.113.10', '203.0.113.10';`
The rule `0.0.0.0 - 0.0.0.0` ("Allow Azure services", named AllowAllWindowsAzureIps) enables
connections from Azure broadly; remove it and use private endpoints instead.

## Database-level rules
Stored in the database (`sys.database_firewall_rules`):
```sql
EXEC sp_set_database_firewall_rule N'app-subnet-nat', '198.51.100.4', '198.51.100.4';
SELECT * FROM sys.database_firewall_rules;
```

## Private endpoint
```bash
az network private-endpoint create -g <rg> -n pe-sql --vnet-name <vnet> --subnet <subnet> \
  --private-connection-resource-id $(az sql server show -g <rg> -n <server> --query id -o tsv) \
  --group-id sqlServer --connection-name pe-sql-conn
az network private-dns zone create -g <rg> -n privatelink.database.windows.net
az network private-dns link vnet create -g <rg> -z privatelink.database.windows.net -n link --virtual-network <vnet> --registration-enabled false
az network private-endpoint dns-zone-group create -g <rg> --endpoint-name pe-sql -n default \
  --private-dns-zone privatelink.database.windows.net --zone-name sql
```
Clients keep using `<server>.database.windows.net`; DNS resolves it via the CNAME to the
`privatelink` private IP. On-premises clients need conditional forwarding for the
`privatelink.database.windows.net` zone.

Then close the public side:
```bash
az sql server update -g <rg> -n <server> --enable-public-network false
```

## Test
```bash
nslookup <server>.database.windows.net     # expect the private IP from inside the VNet
Test-NetConnection <server>.database.windows.net -Port 1433
```
Error 40615 "Client with IP address ... is not allowed" = IP rule missing.
With the Redirect connection policy, clients inside Azure also need ports 11000-11999 to the node.

## Verify
- [ ] No 0.0.0.0 rule; public access disabled or limited to named IPs.
- [ ] Private DNS resolves from every client network, including on-premises.

## Checked
2026-10-28. Confirmed against the firewall-rules, private-link and connectivity-architecture pages: database-level rules checked before server-level rules, 0.0.0.0 rule and AllowAllWindowsAzureIps, sp_set_firewall_rule, sp_set_database_firewall_rule, sys.database_firewall_rules, privatelink.database.windows.net zone and CNAME chain, Redirect ports 11000-11999. The az commands passed check_commands.
Removed unconfirmed claims: virtual network rules in the evaluation order, "private endpoint bypasses IP rules", geo-replica/failover-group travel of database rules, 168.63.129.16, the meaning of error 47073 and the claim that 40615 shows the NAT address.
Method: documentation only; no commands were run.
