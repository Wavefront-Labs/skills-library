---
id: computing-software.cloud-infrastructure-engineering.azure.migrate-dns-zones-to-azure-dns-with-zone-file-import
name: migrate-dns-zones-to-azure-dns-with-zone-file-import
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, azure-dns, zone-file-import, dns-migration, name-server-delegation, dnssec, ttl]
level: practitioner
status: docs-checked
description: "Move a public DNS zone to Azure DNS with no outage: export and import the zone file, verify against Azure name servers, lower TTLs, handle DNSSEC, then switch delegation."
sources: ["https://learn.microsoft.com/azure/dns/dns-import-export", "https://learn.microsoft.com/azure/dns/dns-delegate-domain-azure-dns", "https://learn.microsoft.com/azure/dns/dnssec"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Migrate DNS zones to Azure DNS

**Goal:** change DNS providers for `contoso.com` without a single failed lookup.

## 1. Prepare (days before)
- Lower TTLs at the old provider on frequently changed records (e.g. 300 s) and note the **NS** TTL at the parent.
- Export the zone file in BIND format (most providers offer it; otherwise AXFR if allowed or a script).
- DNSSEC: if the zone is signed at the old provider, plan the DS record at the registrar before switching providers; Azure DNS DNSSEC is described on the DNSSEC page.

## 2. Import
```bash
az network dns zone create -g rg-dns -n contoso.com
az network dns zone import -g rg-dns -n contoso.com -f contoso.com.zone
az network dns record-set list -g rg-dns -z contoso.com -o table
```
- SOA parameters (except host) and the apex NS record set TTL are taken from the imported zone file.
- Provider-specific record types (for example ALIAS/ANAME or URL redirects) are not standard DNS records: recreate them as Azure **alias records** (pointing to Azure resources) or A/AAAA records.

## 3. Verify before switching
```bash
NS=$(az network dns zone show -g rg-dns -n contoso.com --query nameServers[0] -o tsv)
for r in www mail _dmarc @; do dig +short @$NS $r.contoso.com ANY; done
dig +short @$NS contoso.com MX
```
Compare every record against the old provider (script it over the export).

## 4. Switch delegation
At the registrar, replace the name servers with the ones assigned to your Azure DNS zone (for example `ns1-xx.azure-dns.com`, `ns2-xx.azure-dns.net`, `ns3-xx.azure-dns.org`, `ns4-xx.azure-dns.info`).
Keep the old provider's zone live and unchanged until at least the NS TTL has passed (and a few days more).

## 5. After
- Re-enable DNSSEC in Azure DNS (sign the zone, publish the new DS at the registrar).
- Lock the zone (CanNotDelete), grant record-change permissions narrowly, enable diagnostic/activity alerts on record changes.

## Gotchas
- Wildcard and long TXT records (DKIM split strings) need checking after import.
- Delegated subdomains: copy the NS records for child zones too.

## Verify
- [ ] `dig NS contoso.com` from public resolvers returns Azure name servers; record comparisons match; mail flow and websites unaffected.

## Checked
2026-10-28. Confirmed on the DNS import/export, delegate-domain and DNSSEC pages: `az network dns zone import`, SOA parameters except host and apex NS TTL come from the imported zone file, four assigned name servers (`ns1-xx.azure-dns.com`, `.net`, `.org`, `.info`), delegation is set at the registrar, DS records belong to the parent zone.
Fixed: the skill said SOA and NS at the apex are replaced by Azure's. Removed (not confirmed): the 48 h NS TTL, the key-rollover remark, the DNS Zone Contributor role name.

Method: documentation only; no commands were run.
