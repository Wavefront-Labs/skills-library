---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.data-perimeter
name: data-perimeter
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, data-protection, data-perimeter, data-loss-prevention, dlp, exfiltration-prevention, vpc-service-controls, aws-data-perimeter, resource-control-policies, private-endpoints, macie, purview]
level: advanced
status: draft
description: "Prevent exfiltration with a data perimeter: trusted identities, trusted resources and expected networks via org policies, VPC Service Controls, plus DLP discovery."
sources: ["https://docs.aws.amazon.com/whitepapers/latest/building-a-data-perimeter-on-aws/building-a-data-perimeter-on-aws.html", "https://cloud.google.com/vpc-service-controls/docs/overview", "https://learn.microsoft.com/purview/dlp-learn-about-dlp", "https://docs.aws.amazon.com/macie/latest/user/what-is-macie.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Data perimeter and data loss prevention

## The three perimeter questions (AWS data perimeter model)
1. **Trusted identities**: only identities from my organisation can access my resources —
   resource policies / RCPs with `aws:PrincipalOrgID` conditions.
2. **Trusted resources**: my identities can access only my organisation's resources — SCPs /
   VPC endpoint policies with `aws:ResourceOrgID` (stops copying data to an attacker's bucket).
3. **Expected networks**: access only from my networks — `aws:SourceVpc`/`aws:SourceIp`
   conditions, private endpoints.
GCP equivalent: **VPC Service Controls** perimeters around projects with restricted services,
ingress/egress rules, access levels. Azure: private endpoints + disabling public network access,
storage firewall, Azure Policy, Purview DLP for M365/endpoint data.

## DLP discovery
Find sensitive data you didn't know about: Amazon Macie on S3, Google Sensitive Data Protection
(Cloud DLP), Microsoft Purview data map/classification. Feed results into classification tags and access reviews.

## Steps
1. Start with detective mode (log what would be blocked — VPC-SC dry run, policy simulation).
2. Roll perimeter policies out by OU/folder with exceptions for known third parties (documented).
3. Block public access settings at org level (S3 Block Public Access at account level, Azure
   `allowBlobPublicAccess=false`, GCP `storage.publicAccessPrevention`).
4. Alert on perimeter violations.

## Gotchas
- AWS service principals acting on your behalf need `aws:PrincipalIsAWSService` exceptions.
- Perimeters break legitimate SaaS integrations — inventory them first.

## Verify
- [ ] Test copying data from prod to an external account's bucket is denied.
- [ ] Sensitive-data discovery runs on all object storage.
