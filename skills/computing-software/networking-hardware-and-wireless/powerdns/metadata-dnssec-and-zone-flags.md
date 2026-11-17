---
id: computing-software.networking-hardware-and-wireless.powerdns.metadata-dnssec-and-zone-flags
name: metadata-dnssec-and-zone-flags
category: computing-software
field: networking-hardware-and-wireless
product: powerdns
tags: [powerdns, domain-metadata, presigned, nsec3param, publish-cds, soa-edit-api, enable-lua-records]
level: practitioner
status: docs-checked
description: "PowerDNS zone metadata for DNSSEC and behaviour: PRESIGNED, NSEC3PARAM, PUBLISH-CDS, SOA-EDIT, SOA-EDIT-API, API-RECTIFY."
sources:
  - https://raw.githubusercontent.com/PowerDNS/pdns/master/docs/domainmetadata.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Metadata for DNSSEC and zone behaviour

- `PRESIGNED`: `1` marks a zone already carrying RRSIGs. Set automatically when an AXFR brings DNSSEC data; set it by hand for imported zones. API read-only.
- `NSEC3PARAM`: parameters such as `1 0 0 -`; absent means NSEC. `NSEC3NARROW`: `1` enables narrow mode. Both API read-only.
- `PUBLISH-CDNSKEY`: `1` publishes CDNSKEY for KSKs (RFC 7344); default from `default-publish-cdnskey`.
- `PUBLISH-CDS`: comma-separated DNSSEC algorithm numbers; default from `default-publish-cds`.
- `SIGNALING-ZONE`: `1` synthesises CDS/CDNSKEY from other zones (RFC 9615); needs a signed NSEC3-narrow zone (since 5.0.0).
- `SOA-EDIT`: edit mode for the served SOA serial, mainly to make secondaries refresh RRSIGs (API read-only).
- `SOA-EDIT-API`: SOA edit rules for API changes, same rules as `SOA-EDIT-DNSUPDATE`; created as `DEFAULT` with a new zone. Removing it disables SOA editing, which is not the same as `DEFAULT`.
- `SOA-EDIT-DNSUPDATE`, `ALLOW-DNSUPDATE-FROM`, `FORWARD-DNSUPDATE`, `NOTIFY-DNSUPDATE`, `TSIG-ALLOW-DNSUPDATE`: dynamic update controls.
- `ENABLE-LUA-RECORDS`: `1` allows LUA records in the zone even if the global setting is off.
- `API-RECTIFY` (4.1.0+): `1` rectifies after API changes, any other value does not; if unset, `default-api-rectify` decides.
- `RFC1123-CONFORMANCE` (5.1.0+): `0` allows underscores anywhere in names; otherwise RFC 1123 applies.
- `GSS-ACCEPTOR-PRINCIPAL`, `GSS-ALLOW-AXFR-PRINCIPAL`: GSS-TSIG principals.

The HTTP API metadata endpoint cannot read or write `API-RECTIFY`, `ENABLE-LUA-RECORDS` or `SOA-EDIT-API`.

## Checked

2026-11-08. Read in full: PowerDNS docs domainmetadata.rst. Confirmed PRESIGNED, NSEC3PARAM, NSEC3NARROW, PUBLISH-CDNSKEY and PUBLISH-CDS, SIGNALING-ZONE since 5.0.0, SOA-EDIT, SOA-EDIT-API semantics, the dynamic update kinds, ENABLE-LUA-RECORDS, API-RECTIFY, RFC1123-CONFORMANCE since 5.1.0, the GSS kinds and the API access lists. Added the API access note and the API-RECTIFY version.

Method: documentation only; no commands were run.
