---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.multi-account-landing-zone
name: multi-account-landing-zone
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, landing-zone, multi-account, aws-organizations, control-tower, account-factory, aft, organizational-units, azure-landing-zone, management-groups, gcp-landing-zone, folders, hub-and-spoke, transit-gateway, centralised-logging, security-tooling-account, guardrails, scp, break-glass, account-vending, network-segmentation, ipam]
level: advanced
status: draft
description: "Design a multi-account/subscription/project landing zone: OU structure, account vending, central logging and security, guardrails, hub networking, IP planning and break-glass."
sources: ["AWS whitepaper - Organizing Your AWS Environment Using Multiple Accounts", "AWS Control Tower User Guide", "Microsoft Cloud Adoption Framework - Azure landing zones", "Google Cloud Architecture Center - Landing zone design in Google Cloud"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Multi-account landing zone — isolation by default, guardrails by inheritance

**Goal:** a cloud estate where every workload environment is its own account
(subscription/project), security and logging are central and tamper-proof, new
accounts are vended by code in minutes, and policies apply by placement, not by hand.

## 1. Why many accounts
The account is the hardest boundary the provider offers: IAM, quotas, billing,
and blast radius stop at it. One account per **workload per environment** is the
default; shared "prod" accounts with dozens of teams recreate the problems of a
monolith. Equivalents: AWS account, Azure subscription, GCP project.

## 2. Organisational structure (AWS names; Azure management groups and GCP folders mirror it)
```
Root
├── Security        log-archive, security-tooling (audit)
├── Infrastructure  network (hub), shared-services (CI, artifact registry, DNS)
├── Workloads
│   ├── Prod        app1-prod, app2-prod
│   └── NonProd     app1-dev, app1-staging
├── Sandbox         per-developer, budget-capped, no on-prem connectivity
├── Policy-Staging  test guardrail changes here first
└── Suspended       closed/quarantined accounts, deny-all
```
Group OUs by **policy need**, not org chart; reorganisations should not mean moving accounts.
Keep the management/billing account empty of workloads and with very few people.

## 3. Baseline every account gets
- **Identity:** SSO from the corporate IdP (IAM Identity Center / Entra ID / Cloud Identity),
  group-to-role mappings per account. No local users.
- **Logging:** org-wide CloudTrail / Activity Log / Cloud Audit Logs (including data-access
  logs where needed) shipped to the log-archive account, write-once (S3 Object Lock or
  equivalent), retention set by compliance (often 1 year hot, 7 years archive — your
  regulator decides).
- **Security services** with a delegated administrator in security-tooling: GuardDuty,
  Security Hub, Config/Inspector; Defender for Cloud; Security Command Center.
- **Guardrails** (preventive): deny leaving the org, deny disabling logging/security
  tools, region allow-list, deny root-user actions, deny public storage by default.
  Detective guardrails (Config rules, Azure Policy audit, SCC findings) for the rest.
- **Budgets and tags:** budget alerts per account; required tags `owner`, `cost-centre`, `env`, `data-class`.
- Default VPC deleted; EBS/S3 default encryption on; IMDSv2 required.

## 4. Account vending
- AWS: Control Tower Account Factory, **AFT** (Account Factory for Terraform), or
  your own pipeline on `aws organizations create-account`. Azure: subscription vending
  module (ALZ Bicep/Terraform). GCP: project factory module (Cloud Foundation Fabric /
  terraform-google-modules).
- A request (PR with name, OU, owner, budget, CIDR size) produces a ready account with
  baseline, network attachment, SSO assignments and budget in under an hour.

## 5. Networking
- **Hub-and-spoke**: Transit Gateway / Azure Virtual WAN or hub VNet / GCP NCC or Shared VPC.
  Central egress with inspection, central ingress optional per workload.
- **IP plan first:** a non-overlapping supernet per region and environment from 10.0.0.0/8
  (e.g. /16 per region-env, /20-/22 per VPC). Use AWS VPC IPAM or a central registry.
  Overlaps are near-impossible to fix later.
- Private DNS: Route 53 Resolver rules shared via RAM / Azure Private DNS zones linked to hub /
  Cloud DNS peering. Private endpoints for PaaS centralised in DNS.
- Sandbox has internet egress but no route to corporate networks.

## 6. Break-glass and operations
- Two break-glass identities with hardware MFA, credentials in a sealed process,
  exempt from the SSO dependency, every use alerting the security channel.
- Change guardrails via IaC with the Policy-Staging OU as a canary.

## Gotchas
- SCPs/Policies do not apply to the AWS management account; anything there is unguarded.
- Region-deny SCPs must exempt global services (IAM, CloudFront, Route 53, Organizations,
  STS global endpoint, Support) or consoles break in strange ways.
- Account and subscription quotas (e.g. accounts per org, VPCs per region, TGW attachments)
  have defaults that need raising before mass vending — check current limits.
- Closing an AWS account has a post-closure period before it is fully gone; the email
  address cannot be reused immediately. Use plus-addressed or alias mailboxes per account.
- Central egress through a firewall can become the costliest line item (data processing charges).
- Control Tower drift: manual changes to its managed resources break future updates.

## Verify
- [ ] Every workload environment lives in its own account/subscription/project under the right OU.
- [ ] Audit logs from all accounts land in the log-archive store and cannot be deleted by workload admins.
- [ ] A new account request via the vending pipeline is usable without manual steps.
- [ ] IP allocations are recorded centrally and no two VPCs/VNets overlap.
- [ ] Guardrail changes are tested in a staging OU before production OUs.
- [ ] Break-glass login tested in the last 6 months and it raised an alert.

Related: computing-software.cloud-infrastructure-engineering.aws.iam-policies-and-roles, computing-software.cloud-infrastructure-engineering.azure.resource-organisation-and-rbac, computing-software.cloud-infrastructure-engineering.google-cloud.projects-iam-and-service-accounts
