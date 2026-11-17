---
id: computing-software.cloud-infrastructure-engineering.aws.reserved-instances-types-scope-and-marketplace
name: reserved-instances-types-scope-and-marketplace
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, reserved-instances, convertible-ri, zonal-ri, ri-marketplace, regional-ri, size-flexibility, cost-optimization]
level: practitioner
status: docs-checked
description: "Buy and manage EC2 Reserved Instances: Standard vs Convertible, regional vs zonal scope, size flexibility, modification, exchanges, Marketplace sales and discount sharing."
sources: ["https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-reserved-instances.html", "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/apply_ri.html", "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ri-convertible-exchange.html", "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ri-market-general.html", "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ri-modifying.html", "https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/ri-behavior.html", "https://docs.aws.amazon.com/cli/latest/reference/ec2/describe-reserved-instances-offerings.html", "https://docs.aws.amazon.com/cli/latest/reference/ec2/describe-reserved-instances.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# EC2 Reserved Instances: types, scope, marketplace

A Reserved Instance (RI) is a billing discount applied to matching On-Demand usage, not a
physical instance. AWS's own guidance is to **prefer Savings Plans over RIs** for EC2
compute; an RI commits you to a specific instance configuration, a Savings Plan to a
consistent USD-per-hour amount. For current prices see the vendor pricing pages.

## 1. Standard vs Convertible
| | Standard | Convertible |
|---|---|---|
| Discount | most significant | lower than Standard |
| Changing configuration | can only be **modified**; cannot be exchanged | can be **exchanged** for another Convertible RI with a different configuration (instance family, operating system, tenancy), and can also be modified |
| Sell on RI Marketplace | yes | no |

Terms are one year (31536000 s) or three years (94608000 s). Payment options: All Upfront,
Partial Upfront, No Upfront. RIs do not renew automatically; after expiry you pay On-Demand
rates. A purchase cannot be cancelled. The offering class does not change how the discount
is applied.

## 2. Scope
- **Regional**: discount applies in any AZ in the Region and to usage across sizes in the
  instance family (**size flexibility**, based on normalisation factors: large = 4,
  xlarge = 8, 2xlarge = 16, so one 2xlarge RI covers two xlarge). No capacity reservation.
- **Zonal**: specific AZ; attributes (tenancy, platform, AZ, family, size) must match;
  reserves capacity for the owning account only; no size flexibility.
- Size flexibility is not supported for zonal RIs, dedicated tenancy, Windows Server (and
  SQL Server variants), RHEL, SUSE, and some listed families. Check the apply_ri page.

## 3. Operate
```bash
aws ec2 describe-reserved-instances-offerings --instance-type m7i.xlarge --product-description "Linux/UNIX" \
  --offering-class convertible --offering-type "No Upfront" --instance-tenancy default \
  --filters Name=duration,Values=31536000
aws ec2 describe-reserved-instances --filters Name=state,Values=active \
  --query 'ReservedInstances[].[ReservedInstancesId,InstanceType,InstanceCount,Scope,End]' --output table
# Convertible exchange: find offering, get a quote, accept it
aws ec2 get-reserved-instances-exchange-quote --reserved-instance-ids ri-123 --target-configurations OfferingId=<ID>,InstanceCount=2
aws ec2 accept-reserved-instances-exchange-quote --reserved-instance-ids ri-123 --target-configurations OfferingId=<ID>,InstanceCount=2
```
Exchange requirements: the RI is active, has no pending exchange and has at least 24 hours
left; the new RI must be Convertible, in the same Region, and of equal or higher value.
Exchanging is free but may need a true-up payment.

Modify (Standard or Convertible) with `modify-reserved-instances`: change AZ, scope, or
instance size within the same family and generation (Linux/UNIX, default tenancy only for
size). Modification is free, takes effect immediately, and a pending request cannot be
cancelled.

## 4. Selling unused Standard RIs
Only the root user can register as a seller (US-address bank account, tax interview). Only
Standard RIs (regional or zonal) can be sold; at least one month must remain in the term;
No/Partial/All Upfront RIs must have been active at least 30 days; RIs bought with a volume
discount cannot be sold. List with `create-reserved-instances-listing` and a price
schedule. AWS charges a 12 percent service fee on the total upfront price. Lifetime limits
per account: $50,000 and 5,000 RIs. A listing cannot be modified: cancel and relist.

## 5. Sharing
Through consolidated billing in AWS Organizations all accounts can receive the benefit of
RIs bought by any other account; sharing can be turned off on the Billing console
Preferences page. Usage in the purchasing account is matched first.

## Gotchas
- RIs apply only to usage that matches; a Standard RI cannot be exchanged to a different
  family, so prefer Convertible RIs or Savings Plans if a family change is planned.
- Expiry silently reverts the usage to On-Demand pricing; track `End`.

## Verify
- [ ] Every active RI shows utilisation in Cost Explorer.
- [ ] An expiry list exists for all RIs.
- [ ] Planned instance family changes are covered by Convertible RIs or Savings Plans.

## Checked
Date: 2026-11-07
Method: documentation only; no commands were run.
Read in full: Reserved Instances overview (ec2-reserved-instances), How Reserved Instance
discounts are applied (apply_ri, incl. normalisation table), Exchange Convertible Reserved
Instances, Sell Reserved Instances in the Marketplace (restrictions, pricing limits, fee),
Billing "Reserved Instances" sharing page, and the first sections of Modify Reserved
Instances (requirements table; later sections not read). CLI reference pages for
describe-reserved-instances(-offerings) were searched for the `duration` filter and
`Scope`/`End` fields, not read in full; flag names and the `--target-configurations`
members (`OfferingId`, `InstanceCount`) were confirmed from the botocore model.
Removed: "up to ~72%/~66%" discounts, RDS/ElastiCache/OpenSearch/Redshift claim, "regional
is default", "refunds are not available", "95% utilisation" and "60 days notice" thresholds.
