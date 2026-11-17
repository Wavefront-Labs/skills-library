---
id: computing-software.cloud-infrastructure-engineering.azure.app-service-dns-resolution-for-vnet-integrated-apps
name: app-service-dns-resolution-for-vnet-integrated-apps
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, app-service, app-service-dns, website-dns-server, private-dns-zones, vnet-integration, private-endpoints]
level: practitioner
status: docs-checked
description: "Make VNet-integrated App Service and Functions resolve private endpoints: inherited VNet DNS, dnsConfiguration/WEBSITE_DNS_SERVER overrides, zone links and DNS caching."
sources: ["https://learn.microsoft.com/azure/app-service/overview-name-resolution", "https://learn.microsoft.com/azure/app-service/overview-vnet-integration", "https://learn.microsoft.com/azure/private-link/private-endpoint-dns"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DNS for VNet-integrated App Service apps

**Goal:** `myvault.vault.azure.net` resolves to the private endpoint IP from the app, not the public IP.

## How the app resolves names
- Without VNet integration: Azure DNS (public resolution only).
- With regional VNet integration: the app **inherits the VNet's DNS servers** (custom DNS or Azure-provided).
  With Azure-provided DNS, private DNS zones linked to the **integration VNet** are used.
- Override per app: site property `dnsConfiguration.dnsServers` (up to five servers), or the app settings `WEBSITE_DNS_SERVER` /
  `WEBSITE_DNS_ALT_SERVER` (the alternate server answers only when the primary gives no response).
```bash
az webapp config appsettings set -g rg -n app-orders --settings WEBSITE_DNS_SERVER=10.0.0.4 WEBSITE_DNS_ALT_SERVER=10.0.0.5
```

## Hub-and-spoke pattern
- Private DNS zones (`privatelink.vault.azure.net`, `privatelink.database.windows.net`...) linked to the hub;
  spokes use a DNS Private Resolver inbound endpoint or hub DNS forwarders as custom DNS.
- The app's integration subnet's VNet then must have custom DNS = resolver inbound IP. Or link the zones directly to the spoke VNet.
- Outbound traffic to the private IP must go through the integration; private (RFC1918) traffic is routed into the VNet even without route-all.

## Caching and retries
After changing private DNS records an app may keep resolving the old answer until its cache expires or the app restarts; see the name resolution article for the DNS site properties.

## Test from the app
Kudu console (Windows): `nameresolver myvault.vault.azure.net`. Linux SSH: `nslookup myvault.vault.azure.net`.
Expected: CNAME to `myvault.privatelink.vault.azure.net` and a 10.x address.

## Gotchas
- Private DNS zones linked only to the hub, with the spoke on Azure-provided DNS, give public answers -> 403 from
  firewalled services.
- Key Vault references and app content over VNet depend on the same resolution - fix DNS first when they fail.
- Custom DNS servers must forward Azure names to 168.63.129.16 (or the resolver) or private zones are invisible.

## Verify
- [ ] `nameresolver` / `nslookup` from the app returns private IPs for every dependency with a private endpoint.

## Checked
2026-10-27. Confirmed on Microsoft Learn: overview-name-resolution (dnsConfiguration.dnsServers up to five, WEBSITE_DNS_SERVER, WEBSITE_DNS_ALT_SERVER),
overview-vnet-integration (integrated apps use the VNet DNS configuration, private traffic routed without route-all), private-endpoint-dns (privatelink zones).
Removed: `dnsMaxCacheTimeout` default of 30 and the retry property names (not on the fetched page), "route all is default for new apps", `getent` and the nameresolver DNS-argument claim.

Method: documentation only; no commands were run.
