---
id: computing-software.cloud-infrastructure-engineering.external-dns.cloudflare-batch-api-and-tlsa
name: cloudflare-batch-api-and-tlsa
category: computing-software
field: cloud-infrastructure-engineering
product: external-dns
tags: [external-dns, cloudflare-batch-api, batch-change-size, batch-change-interval, cloudflare-tlsa]
level: advanced
status: docs-checked
description: "How the Cloudflare provider batches changes, rolls back and retries per record, which types skip batching, and TLSA caveats (no proxying, DNSSEC)."
sources:
  - https://raw.githubusercontent.com/kubernetes-sigs/external-dns/master/docs/tutorials/cloudflare.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cloudflare batching and TLSA

**Batch API.** All creates, updates and deletes for a zone are grouped into transactional chunks, one API call per chunk, which cuts request count.

- The batch is transactional: if a chunk fails, Cloudflare rolls back the whole chunk. ExternalDNS then retries each change in that chunk individually.
- Types the batch PUT does not support (for example CAA) are always sent individually.
- SRV records use Cloudflare's structured SRV data fields, batched or not.

| Flag | Default | Meaning |
|---|---|---|
| `--batch-change-size` | 200 | Max operations (create, update, delete) per chunk |
| `--batch-change-interval` | 1s | Pause between chunks |

**TLSA.** Add `TLSA` to `--managed-record-types`, because the default set is A, AAAA, CNAME. Targets are `<usage> <selector> <matchingType> <certificate>` in a DNSEndpoint with `recordType: TLSA`. Certificate data is normalised to lowercase hex without separators so written and read-back records compare equal.

- Cloudflare cannot proxy TLSA, so proxying is always off for them regardless of `--cloudflare-proxied`.
- DANE needs DNSSEC: enable it in Cloudflare and add the DS record at the registrar. ExternalDNS does not check.

## Checked

2026-11-04. Read the Cloudflare tutorial (Batch API and TLSA records sections). Confirmed the transactional chunk behaviour, the per-record retry, CAA sent individually, SRV structured fields, the flag defaults 200 and 1s, the TLSA managed-record-types note and the proxying and DNSSEC caveats. Removed the tuning advice, which the page does not give.

Method: documentation only; no commands were run.
