---
id: computing-software.cloud-infrastructure-engineering.external-dns.aws-alias-and-hosted-zone-selection
name: aws-alias-and-hosted-zone-selection
category: computing-software
field: cloud-infrastructure-engineering
product: external-dns
tags: [external-dns, aws-zone-type, aws-target-hosted-zone, aws-hosted-zone-id, aws-zone-match-parent, canonical-hosted-zone]
level: advanced
status: docs-checked
description: "Route53 alias records and zone selection in ExternalDNS: aws-zone-type, alias A or AAAA values, canonical target zone, pinning a hosted zone and aws-zone-match-parent."
sources:
  - https://raw.githubusercontent.com/kubernetes-sigs/external-dns/master/docs/tutorials/aws.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AWS alias records and zone selection

**`--aws-zone-type`:** `public`, `private`, or no value for both.

**Alias annotation.** `external-dns.kubernetes.io/alias: "true"` creates an A and an AAAA ALIAS when the target is itself an alias. Set `A` or `AAAA` to create only one (Route53 provider only). AAAA aliases are created even for load balancers without dualstack; Route53 returns empty sets for them, which is harmless. For an Ingress, the controller needs `--publish-service=<ns>/<controller>` (Helm `controller.publishService.enabled` for ingress-nginx). In the tutorial's Service LoadBalancer example the A and AAAA records come back as alias records.

**`aws-target-hosted-zone`:** `external-dns.kubernetes.io/aws-target-hosted-zone` forces the canonical hosted zone ID used for the ALIAS target. ExternalDNS knows canonical zones for hostnames with known suffixes from `provider/aws/aws.go`; for an unknown suffix add it there or use this annotation.

**`aws-hosted-zone-id`:** `external-dns.kubernetes.io/aws-hosted-zone-id: "Z1234567890ABC"` pins a record to one zone. Use it when public and private zones share a name. If the pinned zone is not configured, the record is skipped.

**`--aws-zone-match-parent`:** lets a subdomain filter match its parent zone. Zone `example.com` with
```text
--domain-filter=x.example.com,example.com
--aws-zone-match-parent
```
creates entries for `x.example.com` and subdomains.

**Verify:** `aws route53 list-resource-record-sets --hosted-zone-id $ZONE_ID --query "ResourceRecordSets[?Name == 'nginx.example.com.']"` shows `AliasTarget` plus a TXT ownership record like `heritage=external-dns,external-dns/owner=...,external-dns/resource=service/default/nginx`.

## Checked

2026-11-04. Read the AWS tutorial (aws-zone-type, alias, target-hosted-zone, hosted-zone-id, aws-zone-match-parent, verification output, Canonical Hosted Zones). Confirmed the zone type values, the alias annotation values and AWS-only note, the publish-service requirement, the AAAA empty-set remark, the canonical zone behaviour, the pin and skip rule, the match-parent example and the TXT ownership record shape. Replaced the unstated claim that Service LoadBalancers get alias records by default with what the tutorial output shows.

Method: documentation only; no commands were run.
