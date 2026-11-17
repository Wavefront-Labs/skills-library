---
id: computing-software.cloud-infrastructure-engineering.google-cloud.migrating-dns-zones-into-cloud-dns
name: migrating-dns-zones-into-cloud-dns
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, cloud-dns, dns-migration, zone-import, bind-zone-file, dnssec]
level: practitioner
status: docs-checked
description: "Move a public zone from another DNS provider into Cloud DNS: create the zone, import a BIND or YAML file, verify against the new name servers, change delegation and handle DNSSEC."
sources: ["https://cloud.google.com/dns/docs/migrating", "https://cloud.google.com/sdk/gcloud/reference/dns/record-sets/import", "https://cloud.google.com/dns/docs/dnssec-config"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Migrating DNS zones into Cloud DNS

## 1. Create the zone and import
```bash
gcloud dns managed-zones create example --dns-name=example.com. --description="migrated" --visibility=public
gcloud dns record-sets import example.zone --zone=example --zone-file-format
gcloud dns record-sets export current.yaml --zone=example        # review
```
- `--zone-file-format` tells import to expect a BIND zone file; without it import expects a YAML records file.
- By default an import fails if an existing record set has the same name and type as one being imported; `--delete-all-existing` makes the imported record sets replace everything in the zone.
- NS records for the zone origin and the SOA NS field are not imported, because Cloud DNS manages its own name servers. An apex NS or SOA record in the import file conflicts with Cloud DNS's own: remove them from the file (recommended), or use `--delete-all-existing` with `--replace-origin-ns` to keep yours.

## 2. Verify before cutover
```bash
NS=$(gcloud dns managed-zones describe example --format='value(nameServers[0])')
for n in www api mail; do diff <(dig +short $n.example.com @$NS) <(dig +short $n.example.com @<OLD_NS>); done
```
Compare every name and type you serve, including MX, TXT, CAA and SRV.

## 3. Cut over
1. Describe the zone to list its name servers (`ns-cloud-*` names; there are shards A to E) and change the authoritative name servers at the **registrar** to them.
2. Note the TTL your registrar has on the records: that is how long you wait before the new servers are used everywhere. Keep the old provider serving until then.

## 4. DNSSEC
For a signed zone the correct DS record must be in the parent zone; an incorrect DS makes DNSSEC resolution fail. Check the configuration with the Verisign DNSSEC debugger, Zonemaster or DNSViz before updating the registrar with the Cloud DNS name servers or DS record. Follow the Cloud DNS DNSSEC migration section for the order of steps.

## Verify
- [ ] `dig NS example.com +trace` shows Cloud DNS servers; if signed, validating resolvers still resolve the name; mail flow and certificate renewals still work.

## Checked
2026-10-28. Confirmed against Cloud DNS Migrate to Cloud DNS, the gcloud `dns record-sets import` reference and the Cloud DNS DNSSEC page: import flags and behaviour, apex NS/SOA handling, name servers `ns-cloud-*` with shards A to E, registrar TTL advice, DS record warning and validation tools. gcloud commands checked with check_commands.py. Removed: `--delete-all-existing` from the first import example, ALIAS/ANAME advice, the fixed 48-hour wait, the specific DNSSEC rollover procedure, TTL-lowering advice, the four-server count wording.
Method: documentation only; no commands were run.
