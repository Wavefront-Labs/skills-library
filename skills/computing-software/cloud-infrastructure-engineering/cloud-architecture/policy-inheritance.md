---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.policy-inheritance
name: policy-inheritance
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, landing-zone, policy-inheritance, management-groups, organizational-units, scp-inheritance, org-policy-hierarchy, policy-exemptions]
level: practitioner
status: draft
description: "Design policy assignment across the resource hierarchy: what applies at root, platform, landing-zone and workload levels, inheritance rules, exemptions and testing."
sources: ["https://learn.microsoft.com/azure/governance/policy/concepts/assignment-structure", "https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_policies_inheritance_auth.html", "https://cloud.google.com/resource-manager/docs/organization-policy/understanding-hierarchy"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Policy hierarchy and inheritance

## Inheritance behaviour
- **Azure Policy**: assignments at management group inherit to all child subscriptions/resource
  groups; exemptions at lower scope; deny wins across assignments.
- **AWS SCPs**: effective permissions are the intersection of SCPs at root, every OU on the path
  and the account - an Allow must exist at every level (FullAWSAccess by default), any Deny wins.
  SCPs do not affect the management account. RCPs (resource control policies) work similarly for resources.
- **Google Org Policy**: inherits down folders/projects; child can merge or replace (inheritFromParent),
  and enforcement can be overridden only where allowed.

## Layering (example)
| Level | Policies |
|---|---|
| Root / org | Allowed regions, deny leaving org, protect security/logging services, require encryption |
| Platform | Allow networking and identity services managed by platform team |
| Landing zones - corp | Deny public IPs, require private endpoints |
| Landing zones - online | Allow public ingress via approved WAF only |
| Sandbox | Budget, SKU restrictions, no hub connectivity |
| Decommissioned | Deny all except read |

## Steps
1. Write policies in code; assign at the highest scope that is correct for all children.
2. Test in a mirror hierarchy (canary management group / OU) before production.
3. Use exemptions with expiry and justification rather than moving resources out of the hierarchy.
4. Monitor compliance per level.

## Gotchas
- Removing FullAWSAccess at an OU without adding allows blocks everything below.
- Policies assigned at subscription level by hand drift from the code.

## Verify
- [ ] Policy-as-code repo is the only source of assignments.
- [ ] Canary hierarchy test passes before rollout.
