---
id: computing-software.cloud-infrastructure-engineering.azure.application-gateway-v1-to-v2-migration
name: application-gateway-v1-to-v2-migration
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, application-gateway, agw-v1-migration, waf-v2, retirement, migration-script]
level: advanced
status: docs-checked
description: "Migrate Application Gateway v1 (retired April 2026) to v2: clone script, subnet and NSG differences, public IP retention, WAF policy conversion and cutover."
sources: ["https://learn.microsoft.com/azure/application-gateway/migrate-v1-v2", "https://learn.microsoft.com/azure/application-gateway/v1-retirement", "https://learn.microsoft.com/azure/application-gateway/configuration-infrastructure"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Application Gateway v1 to v2 migration

**Goal:** get off v1 (Standard/WAF v1 SKUs retired 28 April 2026; Microsoft no longer supports v1 resources and there is no SLA) with a controlled cutover.

## What changes in v2
- Subnet: v2 supports up to 125 instances and a /24 is recommended (v1: up to 32 instances, /26 recommended); NSG must allow
  the GatewayManager service tag on ports **65200-65535** (v1 used 65503-65534).
- v2 brings Key Vault integration, improved WAF capabilities and bot protection; WAF v2 associates WAF policies.
- Backend TLS: v1 authentication certificates become **trusted root certificates** in v2, and v2 enforces certificates more
  strictly. The enhanced script relaxes backend TLS validation by default (no chain, expiry or SNI validation) to avoid
  disruption; tighten it after migration.

## Migration paths
1. **Enhanced cloning script** (`AzureAppGWMigration.ps1`, downloaded from the PowerShell Gallery; the recommended option):
   copies the v1 configuration to a new v2 gateway in a new subnet address range, supports private-only v2 gateways, and can
   remove manual certificate input. Migration has two stages: configuration migration, then traffic migration.
```powershell
AzureAppGWMigration.ps1 -resourceId <v1-gateway-id> -subnetAddressRange 10.0.5.0/24 -appgwName agw-prod-v2 `
  -AppGWResourceGroupName rg-net -sslCertificates $certs -validateMigration -enableAutoScale
```
2. Public IP: `-publicIpResourceId` takes an existing Standard-tier public IP for the v2 gateway; otherwise the script creates
   one named `<AppGwName>-IP`. `-validateMigration` runs basic comparisons (off by default); `-enableAutoScale` enables
   autoscaling (off by default). A private-only v1 needs the `EnableApplicationGatewayNetworkIsolation` feature registered and a
   subnet delegated to `Microsoft.Network/applicationGateways`. Run `Get-Help AzureAppGWMigration.ps1` for the parameters.

## Cutover
- Test v2 with hosts-file overrides or a test hostname; compare responses, headers, WAF behaviour (run WAF in
  Detection first, tune, then Prevention).
- Switch DNS (lower TTL beforehand) or shift traffic gradually with a traffic manager in front.
- Keep v1 until traffic drains; then delete it and its subnet/IP.

## Gotchas
- Authentication certificates (v1) become trusted root certificates for end-to-end TLS in v2.
- Custom error pages and redirects must be re-validated.

## Verify
- [ ] v2 backend health all green and WAF logs reviewed before switching to Prevention.

## Checked
2026-10-28. Confirmed in Learn migrate-v1-v2, v1-retirement and configuration-infrastructure: retirement 28 April 2026 and no support/SLA, 125 versus 32
instance limits and subnet recommendations, GatewayManager port ranges, authentication versus trusted root certificates, relaxed backend
TLS, enhanced script and its parameters, public IP behaviour, private-only prerequisites. Removed: `Install-Script` line, public IP
retention flow (not documented in fetched pages), the 'subject to being stopped' claim, probe-source gotcha, the weighted routing and ARG
query claims.
Method: documentation only; no commands were run.
