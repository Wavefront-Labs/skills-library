---
id: computing-software.networking-hardware-and-wireless.powerdns.http-api-zone-endpoints
name: http-api-zone-endpoints
category: computing-software
field: networking-hardware-and-wireless
product: powerdns
tags: [powerdns, http-api, zones, rrsets, changetype, patch, api-rectify, dnssec]
level: practitioner
status: docs-checked
description: "Use the PowerDNS zone API: list, create, get, PATCH RRsets, delete and rectify endpoints, zone object fields, changetype REPLACE/DELETE/EXTEND/PRUNE, DNSSEC toggling caveats."
sources:
  - https://raw.githubusercontent.com/PowerDNS/pdns/master/docs/http-api/zone.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Zone API endpoints

Under `/api/v1/servers/{server_id}/zones`, with header `X-API-Key`:
- `GET` list and `POST` create (200).
- `GET /{zone_id}` fetch (200); `PATCH /{zone_id}` modify RRsets (204); `DELETE /{zone_id}` (204).
- `PUT /{zone_id}/rectify` returns `{"result": "Rectified"}`.
- `/axfr-retrieve`, `/notify` and `/export` also exist.

Zone object fields: `account`, `api_rectify`, `dnssec`, `edited_serial`, `id`, `kind`, `last_check`, `master_tsig_key_ids`, `masters`, `name`, `notified_serial`, `nsec3narrow`, `nsec3param`, `rrsets`, `serial`, `slave_tsig_key_ids`, `soa_edit`, `soa_edit_api`, `url`; the page's create example also sends `nameservers`. Do not send `serial` or `notified_serial`.

RRset fields: `name`, `type`, `ttl`, `changetype`, `records` (`content`, `disabled`), `comments`.
`changetype`:
- `REPLACE` replaces the RRset; `DELETE` removes it.
- `EXTEND` adds one record, `PRUNE` removes one (added in 4.9.12 and 5.0.2). `EXTEND` is a no-op if the record exists.

Caveats:
- Setting `dnssec` false to true runs the equivalent of `pdnsutil zone secure`, plus a rectify if `api_rectify` is true; this applies to new zones too. If `presigned` is true, nothing DNSSEC-related is changed.
- Rectify after changes on DNSSEC zones, or set `api_rectify` true.
- Invalid record data is rejected; backend-specific features are unsupported.
- For secondary zones avoid sending `nameservers`, `rrsets` or `zone`.
- Comments are per RRset.

## Checked

2026-11-04. Read http-api/zone.rst in full and confirmed the endpoint list, status codes, zone and RRset fields seen in its examples, changetype values with the 4.9.12 and 5.0.2 gate, the dnssec toggle note, rectify advice and secondary zone advice. Reworded the nameservers remark to match the page's create example instead of claiming create-only.

Method: documentation only; no commands were run.
