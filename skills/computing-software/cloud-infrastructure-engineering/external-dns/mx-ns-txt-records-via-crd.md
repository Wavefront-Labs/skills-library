---
id: computing-software.cloud-infrastructure-engineering.external-dns.mx-ns-txt-records-via-crd
name: mx-ns-txt-records-via-crd
category: computing-software
field: cloud-infrastructure-engineering
product: external-dns
tags: [external-dns, mx-record, ns-record, txt-record, managed-record-types-flag]
level: practitioner
status: docs-checked
description: "Manage MX, NS and TXT records with DNSEndpoint objects: required --managed-record-types, target syntax, and provider support limits."
sources:
  - https://raw.githubusercontent.com/kubernetes-sigs/external-dns/master/docs/sources/mx-record.md
  - https://raw.githubusercontent.com/kubernetes-sigs/external-dns/master/docs/sources/ns-record.md
  - https://raw.githubusercontent.com/kubernetes-sigs/external-dns/master/docs/sources/txt-record.md
  - https://raw.githubusercontent.com/kubernetes-sigs/external-dns/master/docs/sources/crd.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MX, NS and TXT via DNSEndpoint

Each type must be enabled with `--managed-record-types`; the default does not manage them.

**MX.** Supported by `aws`, `azure`, `cloudflare`, `google` and `webhook` providers. Targets are `<priority> <host>` per RFC 1034 section 3.6.1.
```console
external-dns --source crd --provider aws --managed-record-types=A --managed-record-types=CNAME --managed-record-types=MX
```
```yaml
spec:
  endpoints:
    - dnsName: example.com
      recordTTL: 180
      recordType: MX
      targets:
        - 10 mailhost1.example.com
        - 20 mailhost2.example.com
```

**NS.** Same pattern with `--managed-record-types=NS`:
```yaml
  - dnsName: zone.example.com
    recordTTL: 300
    recordType: NS
    targets:
    - ns1.example.com
    - ns2.example.com
```
ExternalDNS then creates the NS record through the configured provider.

**TXT.** Needs `--managed-record-types=TXT`; supported by multiple providers including `webhook`. Targets follow RFC 1035 section 3.3.14 (the docs example uses `SOMETXT` and `ANOTHERTXT`). RFC 6763 section 6 is not supported.

```console
external-dns --source crd --provider webhook --managed-record-types=A --managed-record-types=CNAME --managed-record-types=TXT
```

Validation rules for these types are in the DNSEndpoint validation skill.

## Checked

2026-11-04. Confirmed against the ExternalDNS MX, NS and TXT record pages (providers, flags, RFC references, examples) and the CRD Source page (record types not all enabled by default). Nothing removed.
Method: documentation only; no commands were run.
