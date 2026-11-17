---
id: computing-software.systems-network-administration.dns-dhcp.dns-provider-migration
name: dns-provider-migration
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [dns, dns-migration, ttl-lowering, registrar, nameserver-change, ns-records, zone-export, dns-cutover, delegation, migration-validation]
level: practitioner
status: docs-checked
description: "Move a domain to a new DNS provider without an outage: export, lowering TTLs early, parallel serving, the registrar NS change, verification."
sources:
  - https://datatracker.ietf.org/doc/html/rfc1034
  - https://developers.cloudflare.com/dns/zone-setups/full-setup/setup/
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# DNS provider migration

## 1. Inventory and export
- Export the zone (BIND format, provider API, or AXFR if allowed). Watch for provider-specific records that do not export cleanly: ALIAS/ANAME or flattened apex CNAMEs, geo, weighted or failover records, proxied entries (Cloudflare orange cloud), and URL redirect "records".
- Automatic record scans at the new provider are not guaranteed to find everything. Review the apex records, subdomains such as www, and the email records (MX, SPF, DKIM, DMARC) by hand.
- Note DNSSEC status. Cloudflare's setup guide says to turn DNSSEC off at the registrar before replacing nameservers, because changing nameservers while DNSSEC is active can make the domain unreachable; re-enable it through the new provider once the domain is active. If the old provider allows DNSKEY records at the apex, a separate DNSSEC migration procedure exists.

## 2. Lower TTLs in advance
- RFC 1034 notes that a TTL is a time limit on caching and that if a change can be anticipated, the TTL can be reduced prior to the change. Lower record TTLs at least one old-TTL period before the cutover (records with a 24-hour TTL need a day's notice).
- Resolvers also cache the delegation (NS records) held by the parent zone, which you cannot shorten. Plan for both providers to serve identical data until old cached delegations have expired.

## 3. Build and verify the new zone
Before switching, query the old and new authoritative servers directly with `dig` for every name and type and compare the answers. Check SOA, apex NS, MX, TXT (SPF, DKIM, DMARC and any verification records), SRV and CAA.

## 4. Change delegation at the registrar
- Remove the existing authoritative nameservers and add the new provider's exactly as given; if the names are not copied exactly, resolution will break.
- If the old provider stays authoritative in parallel, keep both zones identical and freeze changes until propagation is complete.
- Verify with `dig ns example.com @1.1.1.1`, `dig ns example.com @8.8.8.8` and `dig example.com +trace`, and `whois`. Third-party propagation checkers use cached results and may lag. Cloudflare says to wait up to 24 hours for the registrar update.

## 5. After the old delegation has expired
Confirm traffic on the old provider has stopped (query logs or metrics), then delete the old zone and restore normal TTLs.

## Gotchas
- Glue: if nameserver names are inside the domain being delegated, glue records must exist at the parent and stay consistent with the child NS records (RFC 1034).
- Email: verify SPF, DKIM and DMARC records moved exactly; a missing record breaks mail.
- Activating a domain without the right records gives visitors NXDOMAIN errors.

## Verify
- [ ] No mismatches between old and new before the change; the delegation shows the new NS afterwards.
- [ ] Monitoring or synthetic DNS checks stay green through the transition.

## Checked
Method: docs-checked 2026-11-09 against RFC 1034 (TTL meaning, delegation and glue sections) and the Cloudflare "Set up a primary zone (Full setup)" page, read in full. Dropped the parent TTL figures (such as 172800 s for .com), the octoDNS and DNSControl suggestions, the shell comparison loop and the claim that resolvers cache child-zone NS, none of which were confirmed on those pages.
