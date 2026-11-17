---
id: computing-software.networking-hardware-and-wireless.powerdns.geoip-zone-file-format
name: geoip-zone-file-format
category: computing-software
field: networking-hardware-and-wireless
product: powerdns
tags: [powerdns, geoip, yaml, services, placeholders, weight, custom-mapping]
level: practitioner
status: docs-checked
description: "Write a PowerDNS geoip YAML zone file: domains, records with weight, services and %co %cn %re placeholders, custom_mapping, and which placeholders disable caching."
sources:
  - https://raw.githubusercontent.com/PowerDNS/pdns/master/docs/backends/geoip.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GeoIP zone file format

Root key `domains` is a list; each entry has `domain`, `ttl`, `records`, `services`, `mapping_lookup_formats`, `custom_mapping`. Top-level `mapping_lookup_formats` and `custom_mapping` act as defaults. `zones_dir` can point at a directory of files each holding one `zone:` object.

```yaml
domains:
- domain: geo.example.com
  ttl: 30
  records:
    geo.example.com:
      - soa: ns1.example.com hostmaster.example.com 2014090125 7200 3600 1209600 3600
      - ns: {content: ns1.example.com, ttl: 600}
    swe.eu.service.geo.example.com:
      - a: {content: 192.0.2.3, weight: 50}
  services:
    service.geo.example.com: [ '%co.%cn.service.geo.example.com', '%cn.service.geo.example.com' ]
```

Records are keyed by type (the page's example uses `soa`, `ns`, `mx`, `a`, `aaaa`, `txt`), and a type may appear more than once. Subkeys `content`, `ttl`, `weight` (positive, non-zero; one record per type is picked at random by weight). Every domain needs an apex `soa`.

Placeholders that support EDNS subnet caching: `%co` (three-letter country with the legacy database, ISO3166 country code with MMDB), `%cc` ISO3166 country code, `%cn` continent code, `%af` v4 or v6, `%re` region, `%na` AS organization name, `%as` AS number, `%ci` city, `%loc`, `%lat`, `%lon`, `%%` literal `%`. `%mp` (added in 4.4.0) expands through `mapping_lookup_formats` and `custom_mapping`.

Placeholders that disable caching for that name: `%yy`, `%mos`, `%mo`, `%wds`, `%wd`, `%dd`, `%hh`, `%ip`, `%ip4`, `%ip6`. Use a dedicated name for debugging TXT records.

## Checked

2026-11-04. Read backends/geoip.rst zone file section in full and confirmed the keys, weight rule, apex soa requirement, zones_dir, placeholder lists and non-caching placeholders. Reworded record types as examples from the page rather than a closed list, and separated %mp from the subnet-caching placeholders as the page does.

Method: documentation only; no commands were run.
