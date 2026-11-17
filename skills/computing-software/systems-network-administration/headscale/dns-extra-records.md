---
id: computing-software.systems-network-administration.headscale.dns-extra-records
name: dns-extra-records
category: computing-software
field: systems-network-administration
product: headscale
tags: [headscale, extra-records, a-record, hujson, dns]
level: practitioner
status: docs-checked
description: "Add static or file-based extra DNS records to Headscale MagicDNS, supported file formats, A and AAAA only, and how changes are picked up."
sources:
  - https://raw.githubusercontent.com/juanfont/headscale/main/docs/ref/dns.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Extra DNS records

Static, in `config.yaml` (changes need a Headscale restart):

```yaml
dns:
  extra_records:
    - name: "grafana.myvpn.example.com"
      type: "A"
      value: "100.64.0.3"
```

Dynamic, from a file Headscale watches:

```yaml
dns:
  extra_records_path: /path/to/extra-records.json
```

```json
[
  { "name": "grafana.myvpn.example.com", "type": "A", "value": "100.64.0.3" }
]
```

- `extra_records_path` must be an absolute path.
- Supported extensions: `.json`, `.hujson`, `.yaml`, `.yml`; the extension picks the format. `.json` is read as HuJSON (comments and trailing commas allowed).
- Limitation: Tailscale currently processes only A and AAAA records.
- If a script generates the file, sort keys and give stable output; Headscale uses a checksum to detect changes.

## Verify

```
dig +short grafana.myvpn.example.com
drill -Q grafana.myvpn.example.com
```

Both should return `100.64.0.3` in the docs' example.

## Gotcha

Static entries are processed at startup; the file is processed as Headscale detects changes. The page's motivating example is a reverse proxy on the host, so services can be reached by name without a port.

## Checked

2026-11-04. Confirmed against the Headscale DNS page and config-example.yaml: dns.extra_records, dns.extra_records_path (absolute path), formats and HuJSON, A and AAAA only, checksum-based change detection, and the dig and drill checks.
Method: documentation only; no commands were run.
