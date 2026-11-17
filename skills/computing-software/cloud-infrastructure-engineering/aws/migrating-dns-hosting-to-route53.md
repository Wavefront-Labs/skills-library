---
id: computing-software.cloud-infrastructure-engineering.aws.migrating-dns-hosting-to-route53
name: migrating-dns-hosting-to-route53
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, route53, route53-dns-migration, zone-import, ns-cutover, dnssec-migration, ttl-lowering]
level: practitioner
status: docs-checked
description: "Move a live DNS zone to Route 53 without downtime: export and import records, lower TTLs, compare answers, switch NS at the registrar, and handle DNSSEC safely."
sources: ["https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/MigratingDNS.html", "https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/migrate-dns-domain-in-use.html", "https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/dns-configuring-dnssec-enable-signing.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Migrating DNS hosting to Route 53

This moves the **DNS service** (authoritative zone). Transferring the **domain
registration** is separate and optional; do it later, after DNS is stable.

## 1. Prepare (T minus 2 days or more)
1. Get a full zone export from the current provider (BIND zone file if possible). If no
   export exists, enumerate via `dig` per known name; AXFR is usually disabled.
2. Find the maximum NS TTL at the current provider: the cutover can take that long to
   reach every resolver.
3. Lower the TTLs (including the SOA TTL and SOA minimum field) at the old provider, at
   least one old-TTL period before cutover.

## 2. Create and populate the hosted zone
```bash
aws route53 create-hosted-zone --name example.com --caller-reference mig-$(date +%s) \
  --hosted-zone-config Comment="migrated from oldprovider"
```
Route 53 creates its own NS and SOA; **do not import the old NS/SOA**. Import methods:
- Console "Import zone file" (BIND format; see "Creating records by importing a zone file").
- A script producing `change-resource-record-sets` batches (check the Route 53 quotas
  page for the per-request limits), or records created manually.
Translate provider-specific features:
- ALIAS / ANAME-style records become Route 53 **alias** records, which route to some AWS
  resources such as CloudFront distributions and S3 buckets; use non-alias records for other targets.
- Weighted/geo features map to Route 53 routing policies.

## 3. Verify before cutover
First lower the TTL of the NS record **inside the new Route 53 zone** (the migration guide
recommends 60 to 900 seconds), so that if you must roll back, resolvers drop Route 53 quickly.
Query Route 53's name servers directly and compare with the old provider for every name:
```bash
NS=$(aws route53 get-hosted-zone --id Z123 --query 'DelegationSet.NameServers[0]' --output text)
while read name type; do
  diff <(dig +short @$NS $name $type | sort) <(dig +short @ns1.oldprovider.net $name $type | sort) \
    >/dev/null || echo "MISMATCH $name $type"
done < names.txt
```
Include MX, TXT (SPF/DKIM/DMARC, domain verifications), CAA, SRV and wildcard records.

## 4. DNSSEC
If the zone is DNSSEC-signed at the old provider, a naive NS switch breaks resolution
for validating resolvers (the DS at the parent no longer matches). Safe order:
1. Remove the DS record at the registrar; wait for the DS TTL (and parent caches) to expire.
2. Switch NS (section 5).
3. After stable, enable signing in Route 53 (create a KSK backed by a KMS customer managed
   key) and add the new DS at the parent. Route 53 limits the TTL to 1 week for signed zones.

## 5. Cutover
At the registrar, replace the NS records with the four Route 53 name servers. Keep the
old provider's zone **unchanged and live** for at least the old NS TTL so resolvers
with cached old NS still get correct answers. Monitor with `dig +trace example.com`.

## 6. After
- Raise TTLs back to normal values.
- Raise the Route 53 zone's own NS record TTL back to a more typical value such as 172,800
  seconds (two days), which the guide says improves latency for users.
- Enable query logging if needed; consider registration transfer.

## Gotchas
- Email breaks first: double-check MX and TXT verification records.
- Some providers include hidden records (DKIM selectors managed by email services);
  confirm with the services' admin consoles.


## Verify
- [ ] Every name in the inventory returns identical answers from Route 53 and the old provider before the NS change.
- [ ] `dig NS example.com @a.gtld-servers.net` (or the TLD servers) lists Route 53 name servers after the change.
- [ ] Mail flow, web, and third-party verifications pass after the old NS TTL has expired; old zone then decommissioned.

## Checked

2026-10-28. Confirmed against the Route 53 "make Route 53 the DNS service for an active domain" migration page and the DNSSEC signing page: lower TTLs, SOA TTL and SOA minimum before cutover, find the maximum NS TTL, NS TTL recommended 60-900 seconds then back to e.g. 172800, DS removal before the NS change, KSK with KMS customer managed key, 1-week TTL cap for signed zones, zone file import, alias records route to some AWS resources. Removed (unconfirmed): 1,000-change/32,000-character batch limits, cli53, zone size guidance, TXT 255-character rule, apex CNAME/redirect advice, us-east-1 KMS region, multi-signer note, fixed 48-hour waits. Also removed the private hosted zone gotcha. Read end to end.

Method: documentation only; no commands were run.
