---
id: computing-software.cloud-infrastructure-engineering.aws.s3-data-transfer-pricing-and-same-region-transfer
name: s3-data-transfer-pricing-and-same-region-transfer
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, s3, s3-data-transfer, data-transfer-pricing, gateway-endpoint, cloudfront-origin, nat-gateway-cost]
level: practitioner
status: draft
description: "S3 data transfer costs: free inbound and same-region EC2 access, internet egress tiers, CloudFront origin fetches, NAT processing traps, cross-region replication and acceleration."
sources: ["Amazon S3 pricing - Data transfer", "Amazon VPC User Guide - Gateway endpoints for Amazon S3", "Amazon CloudFront pricing - Origin fetches from AWS origins"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# S3 data transfer pricing

## Matrix (check the pricing page for current rates)
| Path | Transfer charge |
|---|---|
| Internet -> S3 (upload) | free |
| S3 -> EC2/Lambda/ECS in the **same region** | free (requests still billed) |
| S3 -> internet | tiered per GB after the account-wide free allowance |
| S3 -> CloudFront (origin fetch) | free; you pay CloudFront egress (cheaper tiers, commit discounts) |
| S3 -> another region (CRR, direct reads) | inter-region per GB |
| S3 Transfer Acceleration | extra per GB on top |
| Multi-Region Access Points | routing charge per GB plus transfer |
| Via **NAT gateway** from private subnets | NAT processing per GB (and hourly), even though S3 transfer is free |
| Via **gateway endpoint** | free |
| Via interface endpoint (PrivateLink) | endpoint per-GB processing + hourly |

## The usual traps
1. **NAT gateway processing for S3 traffic:** a private-subnet workload reading TBs from S3 pays
   NAT processing per GB. Fix: S3 gateway endpoint on the private route tables (free, minutes to add).
2. **Cross-region reads:** analytics in us-east-1 reading a bucket in eu-west-1; move compute or replicate selectively.
3. **Serving downloads directly from S3** to users: CloudFront in front is usually cheaper and faster; add OAC.
4. **Requester-heavy shared datasets:** enable Requester Pays so consumers in other accounts pay transfer/requests.
5. **Replication of everything:** CRR rules filtered by prefix/tag to what DR actually needs.

## Same-region, cross-account
Accessing a bucket in another account in the same region is free for transfer; requests are billed to
the bucket owner unless Requester Pays.

## Find it in the bill
Cost Explorer: service S3, group by usage type: `*-DataTransfer-Out-Bytes` (internet),
`*-AWS-Out-Bytes`/`*-DataTransfer-Regional-Bytes` (inter-region/region), and on the EC2 side `NatGateway-Bytes`.
S3 Storage Lens and server access logs show which prefixes and requesters drive egress.

## Verify
- [ ] Every VPC with S3 consumers has an S3 gateway endpoint on private route tables.
- [ ] Public downloads go through CloudFront; S3 internet egress trend reviewed monthly.
