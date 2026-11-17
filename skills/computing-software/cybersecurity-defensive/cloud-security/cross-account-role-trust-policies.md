---
id: computing-software.cybersecurity-defensive.cloud-security.cross-account-role-trust-policies
name: cross-account-role-trust-policies
category: computing-software
field: cybersecurity-defensive
product: cloud-security
tags: [iam-least-privilege, cross-account-roles, trust-policy, external-id, confused-deputy, sts-assumerole, third-party-access]
level: practitioner
status: docs-checked
description: "Write safe AWS role trust policies for third parties: ExternalId rules, confused deputy prevention, PrincipalOrgID caveats, and aws:SourceArn/SourceAccount for service principals."
sources: ["https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_common-scenarios_third-party.html", "https://docs.aws.amazon.com/IAM/latest/UserGuide/confused-deputy.html", "https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_condition-keys.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cross-account role trust policies

A trust policy says who can assume a role. For a third party you need their AWS account ID (the Principal), an external ID, and the permissions they need. Give them the role ARN afterwards. They can reach anything the permission policy allows, and their use is billed to you, so scope it tightly.

## Third parties: ExternalId (confused deputy)
Confused deputy: an entity without permission coerces a more privileged one to act. If a SaaS vendor assumes roles in many customers' accounts, a second customer who learns or guesses your role ARN (not a secret) could make the vendor act on your account.
```json
"Principal": {"AWS": "<vendor account id>"},
"Action": "sts:AssumeRole",
"Condition": {"StringEquals": {"sts:ExternalId": "<unique id assigned by vendor>"}}
```
- The vendor generates a unique ID per customer (not the customer); one per customer AWS account is recommended, a random string or GUID. The vendor always includes it in `AssumeRole`.
- It is not a secret: anyone who can view the role sees it.
- 2 to 1,224 characters; alphanumeric, no spaces, plus `+ = , . @ : / -`.
- Vendor practice: test that a customer role cannot be assumed without the correct ID; if it can, do not store the ARN until the customer fixes the trust policy.
- Prefer a role with temporary credentials over giving a third party an IAM user with long-term keys.

## Cross-service confused deputy
A resource policy that trusts a service principal (for example `cloudtrail.amazonaws.com`) with no condition may also accept requests from an unauthorised actor's own configuration. AWS recommends `aws:SourceArn`, `aws:SourceAccount`, `aws:SourceOrgID` or `aws:SourceOrgPaths` whenever a service principal is granted access. `aws:SourceAccount` is only present when a service principal calls directly. Some services have their own controls (KMS grants use encryption context). Resource control policies can apply the check centrally.

## Organisation-scoped trust
`"Condition": {"StringEquals": {"aws:PrincipalOrgID": "o-xxxxxxxxxxx"}}` grants access to every account in an organisation. It is present only for principals in an organisation, also matches the management account, and blocks service principals such as CloudTrail from outside the org; use `aws:PrincipalIsAWSService` (true for direct service-principal calls; use `BoolIfExists` because anonymous requests lack it) to carve those out.

## Audit
IAM Access Analyzer shows whether principals outside your zone of trust (org or account) can assume your roles.

## Verify
Access Analyzer shows no unexpected external role access; assumption by the vendor fails without the correct ExternalId.

## Checked
Method: 2026-11-08 read the third-party access and confused-deputy pages in full and the first 100,000 of ~167,000 characters of the condition-keys page (via summary). Removed unsupported claims: root-principal vs role-ARN guidance, `Principal: *` flagging, session tags/ABAC, MaxSessionDuration and role-chaining limits, SourceIdentity propagation behaviour, CloudTrail audit notes and the role-ID recreation gotcha. The earlier ExternalId policy shape and PrincipalOrgID usage are unchanged.
