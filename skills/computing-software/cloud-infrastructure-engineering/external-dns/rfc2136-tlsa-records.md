---
id: computing-software.cloud-infrastructure-engineering.external-dns.rfc2136-tlsa-records
name: rfc2136-tlsa-records
category: computing-software
field: cloud-infrastructure-engineering
product: external-dns
tags: [external-dns, tlsa-record, dane, rfc2136-tlsa, dnssec-requirement]
level: advanced
status: docs-checked
description: "Publish TLSA (DANE) records through the RFC2136 provider with DNSEndpoint: enabling the type, target format, hex normalisation, AXFR and DNSSEC caveats."
sources:
  - https://raw.githubusercontent.com/kubernetes-sigs/external-dns/master/docs/tutorials/rfc2136.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# TLSA records with RFC2136

TLSA (RFC 6698, the basis of DANE) is supported by the RFC2136 provider. The default managed set is A, AAAA and CNAME only, so add TLSA:

```sh
--managed-record-types=A --managed-record-types=AAAA --managed-record-types=CNAME --managed-record-types=TLSA
```

Targets use RFC 6698 presentation format `<usage> <selector> <matchingType> <certificate>`:

```yaml
apiVersion: externaldns.k8s.io/v1alpha1
kind: DNSEndpoint
metadata:
  name: mail-tlsa
spec:
  endpoints:
    - dnsName: _25._tcp.mail.example.com
      recordType: TLSA
      recordTTL: 300
      targets:
        - 3 1 1 0b9fa5a59eed715c26c1020c711b4f6ec42d58b0015e14337a39dad301c5afc3
```

The certificate association data is normalised to lowercase hex without separators, so records ExternalDNS writes compare equal to the same records read back over AXFR.

**Caveats**
- Reading existing TLSA records needs `--rfc2136-axfr`, like every other type this provider manages. Without it the plan can only create records.
- DANE requires DNSSEC on the zone. Sign it and publish the DS record at your registrar; ExternalDNS does not check this.

**Verify:** `dig TLSA _25._tcp.mail.example.com` against the BIND server returns the record.

## Checked

2026-11-04. Read the RFC2136 tutorial (TLSA records). Confirmed the managed-record-types note, the RFC 6698 target format, the DNSEndpoint example, hex normalisation, the AXFR caveat and the DNSSEC caveat. Removed nothing.

Method: documentation only; no commands were run.
