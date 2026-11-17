---
id: computing-software.cloud-infrastructure-engineering.aws.route53-domain-registration-transfer-and-delegation
name: route53-domain-registration-transfer-and-delegation
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, route53, domain-registration, domain-transfer, ns-delegation, subdomain-delegation, dns-migration]
level: practitioner
status: docs-checked
description: "Register and transfer domains with Route 53, migrate DNS hosting without downtime (TTL lowering, NS cut-over), and delegate subdomains to other hosted zones or accounts."
sources: ["https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/domain-register.html", "https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/domain-transfer-to-route-53.html", "https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/migrate-dns-domain-in-use.html", "https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/CreatingNewSubdomain.html", "https://docs.aws.amazon.com/general/latest/gr/r53.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Route 53 domains: registration, transfer and delegation

Keep three things separate: the **registrar** (who you pay for the name), the **DNS
hosting** (which name servers answer), and **delegation** (NS records pointing to them).

## 1. Migrate DNS hosting first (no downtime)
1. Create the public hosted zone; import records (zone file import in console or
   `change-resource-record-sets` batches). Compare with `dig @old-ns example.com ANY` per name.
2. At the **current** DNS provider, lower the NS-record TTL (typical value is 172800 s, two days; the
   migration guide recommends a short value) and record TTLs, then wait for the old TTL to expire
   (two days when it was 172800).
3. Change the domain's name servers at the registrar to the Route 53 NS from the hosted zone.
4. Monitor, then raise the NS TTL back (172800 s recommended).
DNSSEC: you cannot have DNSSEC signing enabled across two providers at once; **remove the DS record
from the parent zone before** changing name servers, then re-enable signing in Route 53 afterwards.

## 2. Transfer the registration
```bash
aws route53domains check-domain-transferability --domain-name example.com
aws route53domains transfer-domain --domain-name example.com --duration-in-years 1 \
  --auth-code '<EPP_CODE>' --nameservers Name=ns-1.awsdns-01.org Name=... \
  --admin-contact file://contact.json --registrant-contact file://contact.json --tech-contact file://contact.json \
  --privacy-protect-admin-contact --privacy-protect-registrant-contact --privacy-protect-tech-contact
```
Prerequisites: unlocked at the old registrar, EPP/auth code, not registered/transferred in
the last 60 days (transfers are blocked within 60 days of initial registration or a previous
transfer), admin email reachable. The effect on the expiration date varies by TLD (usually one
year is added; see the Transfer Term column of the Route 53 pricing page); status via
`get-operation-detail`. The `route53domains` endpoint is `route53domains.us-east-1.amazonaws.com`,
so use `--region us-east-1`.

## 3. Register new
`aws route53domains register-domain ...` (us-east-1). A hosted zone is created
automatically; enable auto-renew and transfer lock:
`enable-domain-auto-renew`, `enable-domain-transfer-lock`.

## 4. Delegate a subdomain
Create hosted zone `dev.example.com` (often in another account), then in the parent zone:
```bash
aws route53 change-resource-record-sets --hosted-zone-id Z_PARENT --change-batch '{"Changes":[{"Action":"UPSERT","ResourceRecordSet":{"Name":"dev.example.com","Type":"NS","TTL":172800,"ResourceRecords":[{"Value":"ns-111.awsdns-11.com"},{"Value":"ns-222.awsdns-22.net"},{"Value":"ns-333.awsdns-33.org"},{"Value":"ns-444.awsdns-44.co.uk"}]}}]}'
```
Keep the child zone's own NS and SOA records. If the parent's DNS service added an SOA record for
the subdomain, delete it (never the parent's own SOA).

## Gotchas
- Use the four NS values shown in the child hosted zone; if you delete and re-create a zone, re-read them and update the parent or registrar.
- Expired domains with auto-renew off are the classic self-inflicted outage; alarm on expiry
  (`list-domains` returns `AutoRenew`, `TransferLock` and `Expiry` per domain).

## Verify
- [ ] `dig NS example.com +trace` ends at the Route 53 name servers.
- [ ] `dig NS dev.example.com @<parent NS>` returns the child zone NS.
- [ ] `aws route53domains list-domains --region us-east-1` shows `AutoRenew` true and `TransferLock` true for the domain.

## Checked

Checked 2026-10-27 against the Route 53 Developer Guide (register, transfer, migrate DNS, subdomain delegation), the AWS General Reference endpoints page, the aws-cli route53domains reference and the botocore route53domains 2014-05-15 model.
- Corrected: the effect of a transfer on the expiration date varies by TLD (usually one year); DNSSEC advice now follows the migration guide (remove the DS record from the parent, DNSSEC cannot be signed by two providers at once, re-enable after the move); the two-day wait follows the 172800 s NS TTL.
- Confirmed: transfers blocked within 60 days of registration or transfer, `route53domains.us-east-1.amazonaws.com`, transfer-domain and register-domain parameters, `ListDomains` returns AutoRenew, TransferLock and Expiry, hosted zone created at registration.
- Removed: reusable delegation set claim, shadow-record claim and TLD-contact claim that the pages did not support.

Method: documentation only; no commands were run.
