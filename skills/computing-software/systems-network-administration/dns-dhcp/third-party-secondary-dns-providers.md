---
id: computing-software.systems-network-administration.dns-dhcp.third-party-secondary-dns-providers
name: third-party-secondary-dns-providers
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [dns, secondary-dns-provider, multi-provider-dns, zone-transfers]
level: practitioner
status: docs-checked
description: "Add a third-party secondary DNS provider by zone transfer from your primary, and understand the multi-signer DNSSEC models (RFC 8901)."
sources:
  - https://www.rfc-editor.org/rfc/rfc8901
  - https://developers.cloudflare.com/dns/zone-setups/zone-transfers/cloudflare-as-secondary/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Third-party secondary DNS providers

Running a second provider keeps the zone served if one provider has an outage.

## Model
You keep your primary DNS provider and add a secondary. Edits are made at the primary only, and the records are transferred to the secondary by zone transfer, AXFR (full) or IXFR (incremental). Resolvers then query both providers.

Example: Cloudflare supports this as "incoming zone transfers", with a Secondary DNS Override option to proxy traffic through Cloudflare. Per its documentation, Secondary DNS is available only to Enterprise customers.

Practical points that follow from the model:
- The primary must permit transfers to the secondary. Match the secondary provider's transfer settings (source addresses, authentication) to your primary's configuration, following that provider's instructions.
- The registrar delegation and the apex NS records should list the same set of name servers, including the secondary provider's.

## Features that do not transfer
Provider-specific features (ALIAS or flattened records, geo or weighted routing, proxying) are not part of a zone transfer. Confirm with each provider how they are handled.

## DNSSEC with multiple providers (RFC 8901)
RFC 8901 describes "multi-signer" DNSSEC, where several providers each sign the zone. It defines two models:
- Model 1: a common KSK set with a unique ZSK set per provider. Each provider's ZSKs are combined into one DNSKEY RRset that is signed by the shared KSK.
- Model 2: a unique KSK set and ZSK set per provider. Each provider offers an API to import the other providers' ZSKs into its DNSKEY RRset, which each provider signs independently, and the DS RRset at the parent must cover each provider's KSK.
Both need coordination whenever keys roll, since the DNSKEY RRset and DS RRset must be updated across providers. Check that your providers support the model you choose.

## Verify
- [ ] Every name server in the delegation returns the same SOA serial for the zone after a change.

## Checked
Method: docs-checked 2026-11-09 against RFC 8901 (multi-signer models 1 and 2, read in the model sections) and the Cloudflare "Cloudflare as Secondary" page (read in full). The NS1 page is a vendor landing page and was dropped. Removed the BIND TSIG and notify configuration, the Dyn outage reference, the dig nssearch hint and the "sign at the primary and transfer" DNSSEC option, none of which was confirmed by the pages read.
