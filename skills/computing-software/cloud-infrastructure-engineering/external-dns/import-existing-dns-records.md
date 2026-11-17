---
id: computing-software.cloud-infrastructure-engineering.external-dns.import-existing-dns-records
name: import-existing-dns-records
category: computing-software
field: cloud-infrastructure-engineering
product: external-dns
tags: [external-dns, import-records, manual-records, txt-ownership, heritage-external-dns, adopt-records]
level: advanced
status: docs-checked
description: "Adopt manually created DNS records into ExternalDNS by writing matching ownership TXT records, and what happens afterward under sync and upsert-only."
sources:
  - https://raw.githubusercontent.com/kubernetes-sigs/external-dns/master/docs/advanced/import-records.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Importing existing records

Records created by hand (Route 53, Cloud DNS, Azure DNS) are not owned by ExternalDNS. To adopt one, add the TXT records ExternalDNS would have written.

Docs example: `grafana.dev.example.com` is a manual A record to an NLB, referenced by an Istio Gateway; ExternalDNS runs with `--source=istio-gateway`, `--registry=txt`, `--txt-owner-id=dev.example.com`, `--policy=sync`. Create:

```text
aaaa-grafana.dev.example.com  TXT "heritage=external-dns,external-dns/owner=dev.example.com,external-dns/resource=gateway/istio/gateway"
cname-grafana.dev.example.com TXT "heritage=external-dns,external-dns/owner=dev.example.com,external-dns/resource=gateway/istio/gateway"
```

- `external-dns/owner` must equal your `--txt-owner-id`.
- `external-dns/resource` names the owning resource (here Istio's gateway).
- Easiest way to get the exact value: create a dummy record with ExternalDNS and copy its TXT values.

**Then:** wait for the next reconcile. With `policy=sync`, removing the entry from the Kubernetes resource also deletes the provider record. With `policy=upsert-only`, existing records are never deleted.

TXT records are ownership markers that stop multiple controllers colliding. This is useful in migrations where records pre-exist and you want to avoid downtime.

After the reconcile, ExternalDNS should manage the record without errors.

## Checked

2026-11-04. Confirmed against the ExternalDNS Import Existing DNS Records tutorial: the example, TXT values, owner and resource meaning, dummy-record tip, sync and upsert-only behaviour, and notes. Removed an unsourced TXT-prefix bullet and a log-verification line.
Method: documentation only; no commands were run.
