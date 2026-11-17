---
id: computing-software.cloud-infrastructure-engineering.aws.route53-profiles-sharing-dns-configuration
name: route53-profiles-sharing-dns-configuration
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, route53, route53-profiles, private-hosted-zones, resolver-rules, ram]
level: advanced
status: docs-checked
description: "Share private hosted zone associations, Resolver forwarding rules and DNS Firewall rule groups across VPCs and accounts with Route 53 Profiles."
sources: ["https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/profiles.html", "https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/DNSLimitations.html", "https://docs.aws.amazon.com/Route53/latest/APIReference/API_route53profiles_AssociateResourceToProfile.html", "https://docs.aws.amazon.com/cli/latest/reference/route53profiles/index.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Route 53 Profiles

**Problem it solves:** every new VPC needs the same PHZ associations, Resolver rules and DNS Firewall
rule groups; doing it per VPC per account does not scale.

## 1. Build a profile (network account)
```bash
P=$(aws route53profiles create-profile --name corp-dns --query Profile.Id --output text)
PROFILE_ARN=$(aws route53profiles get-profile --profile-id $P --query Profile.Arn --output text)
aws route53profiles associate-resource-to-profile --profile-id $P --name corp-internal \
  --resource-arn arn:aws:route53:::hostedzone/Z0PRIVATE
aws route53profiles associate-resource-to-profile --profile-id $P --name onprem-forward \
  --resource-arn arn:aws:route53resolver:<REGION>:<ACCOUNT_ID>:resolver-rule/rslvr-rr-0abc
aws route53profiles associate-resource-to-profile --profile-id $P --name dns-fw \
  --resource-arn arn:aws:route53resolver:<REGION>:<ACCOUNT_ID>:firewall-rule-group/rslvr-frg-0abc \
  --resource-properties '{"priority":102}'
```

## 2. Share and attach
```bash
aws ram create-resource-share --name corp-dns --resource-arns "$PROFILE_ARN" \
  --principals arn:aws:organizations::<MGMT_ACCOUNT_ID>:ou/o-abc/ou-workloads
# in the consumer account
aws route53profiles associate-profile --profile-id $P --resource-id vpc-0abc --name corp-dns
```
- One profile per VPC. Updating a profile propagates its settings to every associated VPC.
- A profile can be shared with accounts in the same Region through AWS RAM; supported resources
  are private hosted zones, Resolver rules (forwarding and system), DNS Firewall rule groups,
  interface VPC endpoints and Resolver query logging configurations. Reverse DNS lookup for
  Resolver rules, DNS Firewall failure mode and DNSSEC validation are settings managed on the profile.
- Quotas (Route 53 quotas page, read 2026-10-27): 5 profiles per account per Region, 1,000 VPCs per
  profile, 5 DNS Firewall rule groups per profile, 1,000 Resolver rules per profile, 5,000 private
  hosted zones per profile.

## 3. Precedence
- When a query matches both a directly associated VPC setting and a profile setting for the same
  domain, the local VPC setting wins; for conflicting names the most specific domain wins.
- A DNS Firewall rule group added to a profile needs a `priority` between 100 and 9900; the lowest value is processed first.

## Verify
- [ ] From an instance in a consumer VPC, `dig corp.internal` resolves the private zone.
- [ ] `aws route53profiles list-profile-resource-associations --profile-id $P` lists all three resources.

## Checked

Checked 2026-10-27 against the Route 53 Developer Guide (Profiles, quotas), the Route 53 Profiles API Reference and the botocore route53profiles 2018-05-10 model.
- Confirmed: one profile per VPC, supported resource types, precedence (local VPC settings win, most specific domain wins), RAM sharing within a Region, `ResourceProperties` priority 100-9900 for DNS Firewall rule groups.
- Added from quotas page: 5 profiles per account per Region, 1,000 VPCs per profile, 5 DNS Firewall rule groups per profile.
- Corrected: the RAM resource ARN is now read from `get-profile` instead of a hand-built ARN.

Method: documentation only; no commands were run.
