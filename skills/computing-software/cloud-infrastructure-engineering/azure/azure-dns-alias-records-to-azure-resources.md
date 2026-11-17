---
id: computing-software.cloud-infrastructure-engineering.azure.azure-dns-alias-records-to-azure-resources
name: azure-dns-alias-records-to-azure-resources
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, azure-dns, alias-record, alias-records-usage, apex-domain, traffic-manager, front-door, dangling-dns]
level: practitioner
status: docs-checked
description: "Use Azure DNS alias record sets for apex domains and Azure resources (public IP, Traffic Manager, Front Door/CDN, another record set) to avoid dangling DNS and stale IPs."
sources: ["https://learn.microsoft.com/azure/dns/dns-alias", "https://learn.microsoft.com/azure/dns/tutorial-alias-pip", "https://learn.microsoft.com/azure/dns/tutorial-alias-tm", "https://learn.microsoft.com/azure/security/fundamentals/subdomain-takeover"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Azure DNS alias records to Azure resources

**Goal:** DNS records that follow the Azure resource (IP changes, deletion) automatically, and
apex domains (`contoso.com`) that point at Front Door/Traffic Manager despite CNAME rules.

## Supported targets
| Record type | Alias target |
|---|---|
| A / AAAA | Public IP address, Traffic Manager profile (external endpoints only for A/AAAA), Front Door / CDN endpoint, another A/AAAA record set in the same zone |
| CNAME | Another record set in the same zone |

## Create
```bash
# apex -> Front Door
az network dns record-set a create -g rg-dns -z contoso.com -n "@" --target-resource <afd-endpoint-id>
# www -> public IP
az network dns record-set a create -g rg-dns -z contoso.com -n www --target-resource <public-ip-id>
# apex -> Traffic Manager
az network dns record-set a create -g rg-dns -z contoso.com -n "@" --target-resource <tm-profile-id>
```
Portal: Add record set → *Alias record set: Yes* → Azure resource.

## Why it matters
- **Lifecycle tracking**: if the public IP is deleted, the alias returns an empty set instead of pointing at an IP someone else may get — prevents subdomain takeover via dangling records.
- If the public IP changes, the record set updates automatically.
- Lets the zone apex point at load-balanced Azure resources (Traffic Manager, Front Door), because CNAME records are not allowed at the apex.

## Gotchas
- Traffic Manager alias at apex works only for profiles with **external** endpoints (A/AAAA).
- Deleting the target leaves an empty record set; a recreated target has a new resource ID, so IaC must update the alias.

## Verify
- [ ] `az network dns record-set a show -g rg-dns -z contoso.com -n "@" --query targetResource`.
- [ ] `dig contoso.com A` returns the current target IPs; deleting a test public IP empties a test alias record.

## Checked
2026-10-28. Confirmed on the dns-alias and alias tutorial pages: alias targets (public IP, Traffic Manager profile with external endpoints at the apex, Front Door endpoint, another record set of the same type in the same zone), record set becomes empty when the target is deleted, CNAME not allowed at the apex, 50 alias record sets per resource limit. `az network dns record-set a create --target-resource` passed the CLI reference check.
Removed (not confirmed): Standard/Basic IP wording, the private zone note, TTL and free-query claims, the Front Door `_dnsauth` apex steps, cross-subscription and mixed record set gotchas.

Method: documentation only; no commands were run.
