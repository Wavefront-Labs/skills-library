---
id: computing-software.cloud-infrastructure-engineering.aws.guardduty-trusted-ip-and-threat-intel-lists
name: guardduty-trusted-ip-and-threat-intel-lists
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, guardduty, trusted-ip-list, threat-intel-set, threat-detection]
level: advanced
status: docs-checked
description: "Add GuardDuty trusted IP lists to suppress known-good sources and threat intel sets for custom bad IPs, with formats, limits and delegated-admin management."
sources: ["https://docs.aws.amazon.com/guardduty/latest/ug/guardduty_upload-lists.html", "https://docs.aws.amazon.com/cli/latest/reference/guardduty/create-threat-intel-set.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GuardDuty trusted IP lists and threat intel sets

GuardDuty now has two approaches: **entity lists** (recommended; IP addresses, domains or both; API operations `CreateTrustedEntitySet` and `CreateThreatEntitySet`) and legacy **IP lists** (IP addresses only; `create-ip-set`, `create-threat-intel-set`, shown below). IP lists use the GuardDuty service-linked role and need IAM policy updates per Region, which can affect IAM policy size limits. To migrate, add and activate an entity list, then deactivate or delete the IP list. Entity lists and IP lists have different quotas: see the GuardDuty quotas page.

## 1. What each does
| List | Effect | Limit per account per Region |
|---|---|---|
| Trusted list | no findings for activity involving its entries | one trusted entity list and one trusted IP list |
| Threat list | findings when its entries are seen | up to six threat entity lists and threat IP lists |
- Lists apply only to traffic to publicly routable IP addresses and domains.
- Entity list entries apply to CloudTrail, VPC Flow Logs and Route 53 Resolver DNS query log findings; IP list entries apply to CloudTrail and VPC Flow Logs findings, not DNS.
- Only IPv4 addresses are accepted (no IPv6). SHA-256 file hashes work only in threat entity lists. Maximum file size 35 MB.

## 2. Upload (IP list example)
```bash
aws s3 cp trusted.txt s3://sec-lists-<ACCOUNT_ID>/guardduty/trusted.txt
DET=$(aws guardduty list-detectors --query 'DetectorIds[0]' --output text)
aws guardduty create-ip-set --detector-id $DET --name office-egress --format TXT \
  --location https://s3.amazonaws.com/sec-lists-<ACCOUNT_ID>/guardduty/trusted.txt --activate
aws guardduty create-threat-intel-set --detector-id $DET --name partner-feed --format TXT \
  --location https://s3.amazonaws.com/sec-lists-<ACCOUNT_ID>/guardduty/bad.txt --activate
```
IP list formats: `TXT` (one entry per line), `STIX`, `OTX_CSV`, `ALIEN_VAULT`, `PROOF_POINT`, `FIRE_EYE`.
GuardDuty must be able to read the S3 object; see the upload-lists page for the bucket policy and permissions.

## 3. Updating
GuardDuty uses a list only while its status is Active. Whenever you add or update an entry in the S3 object you must activate the list again, for example
`aws guardduty update-threat-intel-set --detector-id $DET --threat-intel-set-id <ID> --activate` (or `update-ip-set`). Activating, deactivating or deleting a list takes an estimated 15 minutes, in some cases up to 40.

## 4. Multi-account
In a multi-account setup only the GuardDuty administrator account manages lists; they apply to the member accounts automatically.

## Gotchas
- Trusting a NAT or proxy IP hides every finding from hosts behind it; trust narrow ranges only.
- An entry on both a trusted and a threat list: the trusted list takes precedence and no finding is generated.

## Verify
- [ ] `aws guardduty get-threat-intel-set` shows `Status: ACTIVE`.
- [ ] A controlled connection to a listed test IP behaves as expected (suppressed for trusted, a finding for threat).

## Checked
2026-10-28. Confirmed on the guardduty upload-lists page and the guardduty botocore model (`IpSetFormat` enum, entity-set operations): list limits, applicability, DNS coverage difference, IPv4-only, hash rule, 35 MB, precedence, re-activation rule, 15/40-minute timing, administrator-only management, SLR remark. Removed as unconfirmed: the `*.Custom` finding type name, the `iam:PutRolePolicy` requirement, scheduled-Lambda advice, the statement about sample findings and custom lists, "private ranges are ignored" (replaced by the documented publicly-routable rule).
Method: documentation only; no commands were run.
