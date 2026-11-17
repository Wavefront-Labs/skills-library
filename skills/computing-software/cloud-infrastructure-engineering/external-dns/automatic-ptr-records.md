---
id: computing-software.cloud-infrastructure-engineering.external-dns.automatic-ptr-records
name: automatic-ptr-records
category: computing-software
field: cloud-infrastructure-engineering
product: external-dns
tags: [external-dns, create-ptr, ptr-records, reverse-dns, in-addr-arpa, record-type-annotation]
level: practitioner
status: docs-checked
description: "Create reverse DNS with ExternalDNS: --create-ptr, the record-type ptr annotation and opt-out, required flags, DNSEndpoint usage, and wildcard and multi-hostname behaviour."
sources:
  - https://raw.githubusercontent.com/kubernetes-sigs/external-dns/master/docs/advanced/ptr-records.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Automatic PTR records

`--create-ptr` (boolean, default `false`) sets the global default; the annotation `external-dns.kubernetes.io/record-type` overrides per resource.

| Flag | Annotation | Result |
|---|---|---|
| true | absent | PTR created |
| true | `""` | not created (opt out) |
| false | absent | not created |
| false | `"ptr"` | created (opt in) |

**Prerequisites:** the provider must have authority over the reverse zone, that zone must be in `--domain-filter`, and PTR must be in `--managed-record-types`:

```sh
--create-ptr --managed-record-types=A --managed-record-types=AAAA \
--managed-record-types=CNAME --managed-record-types=PTR \
--domain-filter=example.com --domain-filter=49.168.192.in-addr.arpa
```

With a Service annotated `record-type: "ptr"` and external IP `192.168.49.2`, you get `web.example.com` A and `2.49.168.192.in-addr.arpa` PTR.

**DNSEndpoint** ignores annotations; set it in the spec:
```yaml
providerSpecific:
- name: record-type
  value: ptr
```

**Behaviour**
- Wildcard records are skipped.
- Several hostnames on one IP become multiple PTR records in one RRSet (`dig -x` returns two answers). Not every provider handles multi-target PTR; check yours.
- PTR records whose forward hostname no longer matches `--domain-filter` are cleaned up.
- PTRs are tracked by the TXT registry like other types.

## Checked

2026-11-04. Confirmed against the ExternalDNS Automatic PTR Records page: flag default and table, prerequisites and example flags, the Service example, DNSEndpoint providerSpecific usage, and the behaviour list. Nothing removed.
Method: documentation only; no commands were run.
