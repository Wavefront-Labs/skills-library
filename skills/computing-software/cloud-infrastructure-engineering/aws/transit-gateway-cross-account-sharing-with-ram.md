---
id: computing-software.cloud-infrastructure-engineering.aws.transit-gateway-cross-account-sharing-with-ram
name: transit-gateway-cross-account-sharing-with-ram
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, transit-gateway, tgw-ram-sharing, tgw-cross-account, resource-access-manager, multi-account, network-account]
level: practitioner
status: docs-checked
description: "Share a central Transit Gateway with workload accounts via RAM: org/OU shares, attachment acceptance, routing control and attachment lifecycle states."
sources: ["https://docs.aws.amazon.com/vpc/latest/tgw/tgw-transit-gateways.html", "https://docs.aws.amazon.com/vpc/latest/tgw/tgw-vpc-attachments.html", "https://docs.aws.amazon.com/ram/latest/userguide/shareable.html", "https://docs.aws.amazon.com/whitepapers/latest/building-scalable-secure-multi-vpc-network-infrastructure/transit-gateway.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Sharing a Transit Gateway across accounts

**Goal:** one TGW owned by a network account; workload accounts attach their VPCs.

## Why this pattern
- AWS guidance: place the organisation's Transit Gateway in a Network Services account and use AWS RAM to share it
  with VPCs in other accounts of the AWS Organization within the same Region. A transit gateway is a Regional
  resource; one per Region usually suffices (it is highly available by design), with multiple gateways justified to
  limit misconfiguration blast radius or segregate control plane operations.
- RAM can share a transit gateway (`ec2:TransitGateway`) with any AWS account or with the organisation. To include it
  in a share you need `ec2:DescribeTransitGateway` in addition to `ram:CreateResourceShare`.

## 1. Share
```bash
aws ram create-resource-share --name core-tgw \
  --resource-arns arn:aws:ec2:<REGION>:<NET_ACCOUNT>:transit-gateway/tgw-123 \
  --principals arn:aws:organizations::<MGMT_ACCOUNT>:organization/o-abc123 \
  --no-allow-external-principals
```
Recipients outside the organisation accept the resource share invitation
(`aws ram accept-resource-share-invitation`); the TGW guide has "Accept a resource share" and "Accept a shared
attachment" tasks.

## 2. Attach from the workload account
```bash
aws ec2 create-transit-gateway-vpc-attachment --transit-gateway-id tgw-123 --vpc-id vpc-app \
  --subnet-ids subnet-tgw-a subnet-tgw-b
```
- Specify one subnet from each Availability Zone that needs to reach the TGW; resources in an AZ without an
  attachment subnet cannot reach it. Attachment subnets must support IPv4 (no IPv6-only subnets) and cannot be in a
  Local Zone.
- If the TGW has "Auto accept shared attachments" turned off, a cross-account attachment waits in
  `pending-acceptance` until the TGW owner accepts it:
```bash
aws ec2 accept-transit-gateway-vpc-attachment --transit-gateway-attachment-id tgw-attach-xyz
```
  After acceptance it goes `pending` then `available`. A rejected or deleted attachment stays visible for 2 hours.
- A new attachment is associated with the default TGW route table. To segment (for example development versus
  production VPCs) create additional route tables in the transit gateway and move the association; propagation can be
  enabled or disabled per attachment. These are TGW-level settings.

## 3. Constraints to plan for
- After the share, the account owner can attach VPCs, and a user from either account can delete the attachment at any
  time.
- The TGW does not route between VPCs with identical or overlapping CIDRs: routes for the newly attached VPC are not
  propagated.
- No DNS resolution for private hosted zone names of attached VPCs through the TGW.
- Attachment subnets need route entries for in-VPC destinations, and workload subnets need routes to the TGW for
  return traffic.

## Gotchas
- Automation of attachment approval is a design choice; the AWS whitepaper points to an AWS blog on automating
  attachments to a transit gateway in a central account.
- For pricing of attachments and data processing see the Transit Gateway pricing page; it is not stated in these pages.

## Verify
- [ ] The cross-account attachment shows `pending-acceptance` (auto accept off), then `available` after acceptance.
- [ ] The attachment is associated with the intended TGW route table, and routes are propagated.

## Checked
2026-11-08. Confirmed against the Transit Gateway guide pages on transit gateways and VPC attachments, the RAM
shareable-resources table and the AWS multi-VPC whitepaper; CLI commands checked against the botocore model.
Removed: org-share auto-accept claim, the attachment-owner billing claim, claims about tag visibility, the network
versus workload visibility table, the SCP suggestion, the EventBridge automation recipe and the describe-transit-gateways
OwnerId check, none of which the pages state.
Method: docs-only read of cited pages, 2026-11-08
