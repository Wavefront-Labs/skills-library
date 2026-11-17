---
id: computing-software.cloud-infrastructure-engineering.aws.availability-zone-ids-vs-names
name: availability-zone-ids-vs-names
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, availability-zones, az-id, availability-zone-id, multi-az, resource-access-manager, zonal-shift]
level: practitioner
status: docs-checked
description: "Use AZ IDs, not names, across accounts: why us-east-1a differs per account, how to map names to IDs, and where AZ IDs matter (RAM, PrivateLink, zonal shift)."
sources: ["https://docs.aws.amazon.com/ram/latest/userguide/working-with-az-ids.html", "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-regions-availability-zones.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AZ IDs vs AZ names

## The problem
AWS maps physical AZs to AZ **names** (`us-east-1a`) randomly for each account, to distribute
resources across zones. `us-east-1a` in one account might not be the same physical location as
`us-east-1a` in another. The AZ **ID** (`use1-az1`) is the same in every account.

## Map names to IDs
```bash
aws ec2 describe-availability-zones --region us-east-1 \
  --query 'AvailabilityZones[].[ZoneName,ZoneId,ZoneType]' --output table
aws ec2 describe-subnets --query 'Subnets[].[SubnetId,AvailabilityZone,AvailabilityZoneId]' --output table
```
Create subnets by ID to make IaC consistent across accounts:
```bash
aws ec2 create-subnet --vpc-id vpc-0abc --cidr-block 10.0.1.0/24 --availability-zone-id use1-az4
```

## Where IDs matter
- **Shared VPCs (RAM):** a subnet shared from the zone with AZ ID `use1-az2` is available to the other
  account in the zone whose AZ ID is also `use1-az2`, whatever that account calls it. The AZ ID of each
  subnet is shown in the VPC console and CLI.
- **Cross-account placement:** compare AZ IDs, not names, to tell whether resources in two accounts are in the same zone.
- Instance type availability varies by zone; query it by AZ ID with `describe-instance-type-offerings --location-type availability-zone-id`.

## Practices
- Record AZ IDs, not names, in architecture docs and runbooks.
- Build subnets by AZ ID so IaC is consistent across accounts.

## Gotchas
- Moving a workload to another account with "the same AZ name" can silently change its physical zone.

## Verify
- [ ] Subnet IaC uses AZ IDs; a table of name-to-ID per account exists.
- [ ] Cross-account dependencies documented by AZ ID.

## Checked

2026-10-28. Confirmed against the RAM "Availability Zone IDs for your AWS resources" page, the EC2 Regions and Zones page and the ec2 botocore model: random per-account name mapping, AZ IDs identical across accounts, shared subnet availability by AZ ID, describe-availability-zones output fields (ZoneName, ZoneId, ZoneType), DescribeInstanceTypeOfferings LocationType enum including availability-zone-id. Removed (unconfirmed): CloudFormation/Terraform property names, cross-AZ charge and latency claims, PrivateLink, zonal shift/Health/FIS claims, capacity reservation/Local Zone/MSK/Redshift claim, the "newer regions" remark. Read end to end.

Method: documentation only; no commands were run.
