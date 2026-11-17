---
id: computing-software.cloud-infrastructure-engineering.aws.route53-ttl-tuning-and-record-types
name: route53-ttl-tuning-and-record-types
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, route53, dns-ttl, cname-record, alias-record, dns-records]
level: practitioner
status: docs-checked
description: "Pick Route 53 record types and TTLs: alias vs CNAME at the apex, lowering TTLs before migrations, negative caching via SOA and checking with dig."
sources: ["https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/resource-record-sets-choosing-alias-non-alias.html", "https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/ResourceRecordTypes.html", "https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/SOA-NSrecords.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# TTL tuning, CNAME vs alias, record types

## 1. Alias vs CNAME
| | Alias | CNAME |
|---|---|---|
| Zone apex (`example.com`) | yes | no (RFC: cannot coexist with SOA/NS) |
| Targets | ELB, CloudFront, API GW, S3 website, Global Accelerator, VPC endpoint, another record in the zone | any hostname |
| Query charge | free for AWS-resource targets | charged |
| TTL | inherited from target (you cannot set it) | you set it |
| Health | `EvaluateTargetHealth` | via health check only |
A CNAME name cannot have any other record type.

## 2. TTL strategy
- Steady state: 300-3600 s for stable records; 60 s for failover/weighted records.
- Migration: lower the TTL to 60 s at least one old-TTL period **before** the change, change, then raise.
- NS records at the registrar/parent: 172,800 s by default, so delegation changes take up to 2 days.
- Negative answers (NXDOMAIN or NODATA) are cached for the lesser of the SOA minimum TTL (last SOA
  field, 86400 s in the documented example) and the SOA record's own TTL (default 900 s). Route 53 bills
  negative responses like normal queries; lower these values if clients look names up before you create them.

## 3. Change
```bash
cat > c.json <<'J'
{"Changes":[{"Action":"UPSERT","ResourceRecordSet":{"Name":"app.example.com","Type":"CNAME","TTL":60,
 "ResourceRecords":[{"Value":"new-lb-123.<REGION>.elb.amazonaws.com"}]}}]}
J
aws route53 change-resource-record-sets --hosted-zone-id Z123 --change-batch file://c.json
aws route53 get-change --id <CHANGE_ID>   # INSYNC = on all Route 53 servers
```

## 4. Record types quick reference
A/AAAA, CNAME, MX (priority + host), TXT (SPF, DKIM, verification; a string holds up to 255 characters, split longer values; 4,000 characters maximum per record value),
SRV, CAA (which CAs may issue), NS, SOA, PTR (reverse zones), DS (DNSSEC delegation).

## Verify
- [ ] `dig +noall +answer app.example.com @ns-123.awsdns-45.com` shows the new value and TTL.
- [ ] `dig app.example.com @1.1.1.1` TTL counts down from the new value after the old TTL expires.

## Checked

Checked 2026-10-27 against the Route 53 Developer Guide (alias vs non-alias records, record types, SOA and NS records).
- Corrected: negative caching lasts the lesser of the SOA minimum TTL and the SOA record's own TTL (default 900 s); the 86400 s value is the documented example, not a default.
- Confirmed: alias queries to AWS resources are not charged, CNAME queries are charged, alias TTL cannot be set, TXT strings up to 255 characters and 4,000 characters per record value, NS TTL 172800 s.

Method: documentation only; no commands were run.
