---
id: computing-software.cloud-infrastructure-engineering.external-dns.dnsendpoint-validation-and-status
name: dnsendpoint-validation-and-status
category: computing-software
field: cloud-infrastructure-engineering
product: external-dns
tags: [external-dns, dnsendpoint-validation, status-conditions, partially-invalid, crd-limits, duplicate-endpoints]
level: advanced
status: docs-checked
description: "DNSEndpoint validation: schema limits at apply time, read-time checks per record type, the Accepted and PartiallyInvalid status conditions, and duplicate-name conflicts."
sources:
  - https://raw.githubusercontent.com/kubernetes-sigs/external-dns/master/docs/sources/crd.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DNSEndpoint validation and status

**Schema, at `kubectl apply`**
- `dnsName` and `recordType` required; wildcard `*.` and `_`-prefixed labels allowed; at most 253 characters (254 with a trailing dot).
- `recordType` one of A, AAAA, CNAME, TXT, SRV, NS, PTR, MX, NAPTR.
- `recordTTL` 0 to 2147483647; `0` means unset.
- Targets 1 to 4096 characters; at most 1000 targets per endpoint, 1000 endpoints per object, 100 `providerSpecific` entries.
- SRV and NAPTR targets must be absolute (trailing dot). PTR `dnsName` sits under `.in-addr.arpa` or `.ip6.arpa` without a trailing dot.
- Over any limit the whole object is rejected. Split across objects, keeping a record in one object.

**Read-time checks (bad endpoint dropped, others published)**
- A/AAAA targets must match the family unless the `alias` provider-specific property is set.
- MX: `<preference> <host>`. SRV: `<priority> <weight> <port> <host>`.
- PTR needs a non-empty target.
- Other types reject a trailing dot (CNAME and TXT allow both).
- Empty `targets` only with `--default-targets`.

**Duplicates:** two objects with the same `dnsName` and `recordType` conflict; one is published, the other dropped, with no merge.

**Status**
```console
$ kubectl get dnsendpoint
NAME               ACCEPTED   AGE
examplednsrecord   True       2m
```
`Accepted` Unknown/Pending (unread), True (at least one endpoint planned), False/Invalid (all refused; message names each index). `PartiallyInvalid` True/Invalid means some were dropped. `Accepted` is set before provider calls, so it does not prove records exist.

## Checked

2026-11-04. Confirmed against the ExternalDNS CRD Source page (Validation and Status sections): schema limits, read-time checks, duplicate conflict and the condition table. Nothing removed.
Method: documentation only; no commands were run.
