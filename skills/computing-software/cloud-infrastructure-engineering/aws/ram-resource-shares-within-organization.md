---
id: computing-software.cloud-infrastructure-engineering.aws.ram-resource-shares-within-organization
name: ram-resource-shares-within-organization
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, ram, ram-org-sharing, resource-share, resource-access-manager, organizations]
level: practitioner
status: docs-checked
description: "Share subnets, TGWs, prefix lists and Resolver rules with OUs through AWS RAM, enable org sharing, pick managed permissions and block external principals."
sources: ["https://docs.aws.amazon.com/ram/latest/userguide/getting-started-sharing.html", "https://docs.aws.amazon.com/ram/latest/userguide/shareable.html", "https://docs.aws.amazon.com/ram/latest/userguide/security-scp.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# RAM resource shares within the organization

## 1. Enable once (management account)
```bash
aws ram enable-sharing-with-aws-organization
```
With sharing within the organization enabled, principals in the organization that you share with are granted access without invitations.

## 2. Create a share (resource owner account)
```bash
aws ram create-resource-share --name shared-network \
  --resource-arns arn:aws:ec2:<REGION>:<ACCOUNT_ID>:subnet/subnet-0abc arn:aws:ec2:<REGION>:<ACCOUNT_ID>:transit-gateway/tgw-0abc \
  --principals arn:aws:organizations::<MGMT_ACCOUNT_ID>:ou/o-abc123/ou-abcd-1234 \
  --no-allow-external-principals
aws ram list-permissions --resource-type ec2:Subnet           # managed permissions available
aws ram get-resource-share-associations --association-type PRINCIPAL --resource-share-arns <ARN>
```
- Accounts added to a shared OU or the organization get access automatically; accounts removed from it lose access.
- Choose or create a **customer managed permission** when the default grants too much. If a managed permission has multiple versions, RAM attaches the default version.

## 3. Commonly shared types
Subnets (VPC sharing), Transit Gateways, Route 53 Resolver rules, managed prefix lists, IPAM pools,
License Manager configs, Network Firewall policies, Capacity Reservations, Aurora DB clusters (for clones),
Glue catalogs.

## 4. Guardrail
SCP to stop sharing outside the org:
```json
{"Effect":"Deny","Action":["ram:CreateResourceShare","ram:UpdateResourceShare"],"Resource":"*",
 "Condition":{"Bool":{"ram:RequestedAllowsExternalPrincipals":"true"}}}
```

## Gotchas
- RAM is a Regional service: principals can use shared resources only in the Region where they were created, so create shares per Region (global resources are viewed in us-east-1).
- Without org sharing enabled, each account must accept an invitation (`accept-resource-share-invitation`); invitations expire (12 hours for most resource types, seven days for some).
- Before deleting a resource that is in a share, remove it from the share or delete the share.
- For account-to-account sharing in an organization, `RetainSharingOnAccountLeaveOrganization` keeps access when an account leaves.

## Verify
- [ ] In a consumer account `aws ram list-resources --resource-owner OTHER-ACCOUNTS` shows the resources.
- [ ] `allowExternalPrincipals` is false on every share.

## Checked

2026-10-28. Confirmed against the RAM user guide pages (getting started with sharing, shareable resources, SCP guardrails): `enable-sharing-with-aws-organization`, no invitations inside an enabled organization, OU membership changes, default managed-permission version, Regional service, invitation expiry, RetainSharingOnAccountLeaveOrganization, ram:RequestedAllowsExternalPrincipals condition key in the SCP example, and that subnets, transit gateways, Resolver rules, prefix lists, IPAM pools, License Manager, Network Firewall policies, capacity reservations, RDS clusters and Glue catalogs appear in the shareable resources list. Removed (unconfirmed): consumers cannot modify/billing claim. Read end to end.

Method: documentation only; no commands were run.
