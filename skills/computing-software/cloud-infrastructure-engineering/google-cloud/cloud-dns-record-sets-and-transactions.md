---
id: computing-software.cloud-infrastructure-engineering.google-cloud.cloud-dns-record-sets-and-transactions
name: cloud-dns-record-sets-and-transactions
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, cloud-dns, gcloud-dns-record-sets, dns-transaction, ttl, change-management]
level: practitioner
status: docs-checked
description: "Manage Cloud DNS records safely with gcloud: record-sets create/update/delete, atomic transactions, TXT/MX/CAA quoting, TTL lowering before changes, and change history."
sources: ["https://cloud.google.com/dns/docs/records-overview", "https://cloud.google.com/sdk/gcloud/reference/dns/record-sets", "https://cloud.google.com/sdk/gcloud/reference/dns/record-sets/transaction", "https://cloud.google.com/sdk/gcloud/reference/dns/record-sets/changes/list"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cloud DNS record sets and transactions

## 1. Single-record operations
```bash
gcloud dns record-sets create www.example.com. --zone=example --type=A --ttl=300 --rrdatas=203.0.113.10
gcloud dns record-sets update www.example.com. --zone=example --type=A --ttl=300 --rrdatas=203.0.113.20
gcloud dns record-sets delete old.example.com. --zone=example --type=CNAME
gcloud dns record-sets list --zone=example --name=www.example.com. --type=A
```
A record set is all records of one name+type: `update` replaces the whole set (list every value).

## 2. Quoting
```bash
gcloud dns record-sets create example.com. --zone=example --type=TXT --ttl=300 \
  --rrdatas='"v=spf1 include:_spf.google.com ~all"','"google-site-verification=abc"'
gcloud dns record-sets create example.com. --zone=example --type=MX --ttl=3600 \
  --rrdatas='1 smtp.google.com.'
gcloud dns record-sets create example.com. --zone=example --type=CAA --ttl=3600 \
  --rrdatas='0 issue "pki.goog"','0 issue "letsencrypt.org"'
```
A TXT record may hold several strings of at most 255 characters each, every string in quotation marks (DKIM keys); each TXT record has a 1,000-character limit. The SPF record type is deprecated: use TXT records starting with `v=spf1`. MX data must end with a dot.

## 3. Atomic multi-record changes (transactions)
```bash
gcloud dns record-sets transaction start --zone=example
gcloud dns record-sets transaction remove --zone=example --name=api.example.com. --type=A --ttl=300 203.0.113.10
gcloud dns record-sets transaction add    --zone=example --name=api.example.com. --type=A --ttl=60  198.51.100.7
gcloud dns record-sets transaction execute --zone=example     # or abort
```
`transaction remove` takes the record data as positional arguments plus `--name`, `--ttl` and `--type`; `describe` shows the pending change and `abort` discards it. The transaction
file (default `transaction.yaml`, set with `--transaction-file`) is local; don't leave stale ones around.

## 4. Change discipline
- Lower TTL to 60 s at least one old-TTL period before a cutover; raise it afterwards.
- `gcloud dns record-sets changes list --zone=example` lists the changes made to the zone's record sets.
- Manage zones in Terraform (`google_dns_record_set`) for anything long-lived.

## Verify
- [ ] `dig +short www.example.com @NAME_SERVER` (one of the zone's name servers) returns the new value; public resolvers follow after the old TTL.

## Checked

- Date: 2026-10-27; documentation release: Google Cloud documentation pages as published on that date.
- Confirmed (record types page): TXT strings up to 255 characters each in quotation marks and a 1,000-character limit per TXT record, SPF type deprecated, MX data must end with a dot, CAA record type.
- Confirmed (gcloud reference): `record-sets create/update --rrdatas --ttl --type --zone`, `transaction start/add/remove/describe/abort/execute` with `--transaction-file` default transaction.yaml, `transaction remove` requires --name, --ttl and --type, `changes list --zone`.
- Removed: the claim that a mismatched remove makes execute fail, the audit-log attribution for change history and a nameserver hostname that was not documented for public zones.

Method: documentation only; no commands were run.
