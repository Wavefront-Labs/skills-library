---
id: computing-software.cybersecurity-defensive.cloud-security.aws-tag-based-abac
name: aws-tag-based-abac
category: computing-software
field: cybersecurity-defensive
product: cloud-security
tags: [aws-abac, attribute-based-access-control, aws-principaltag, resource-tags, session-tags, tag-policies, cloud-iam]
level: advanced
status: docs-checked
description: "Implement tag-based ABAC in AWS: principal and resource tag matching, session tags from the IdP, protecting tags from tampering, and services that do not support it."
sources: ["https://docs.aws.amazon.com/IAM/latest/UserGuide/introduction_attribute-based-access-control.html", "https://docs.aws.amazon.com/IAM/latest/UserGuide/id_session-tags.html", "https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_aws-services-that-work-with-iam.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tag-based ABAC in AWS

One policy grants access when the principal's tag equals the resource's tag, instead of a role per
project.

## Policy pattern
```json
{
  "Effect": "Allow",
  "Action": ["ec2:StartInstances", "ec2:StopInstances"],
  "Resource": "*",
  "Condition": {"StringEquals": {"aws:ResourceTag/project": "${aws:PrincipalTag/project}"}}
},
{
  "Effect": "Allow",
  "Action": ["ec2:RunInstances", "ec2:CreateTags"],
  "Resource": "*",
  "Condition": {"StringEquals": {"aws:RequestTag/project": "${aws:PrincipalTag/project}"},
                "ForAllValues:StringEquals": {"aws:TagKeys": ["project", "owner"]}}
}
```

## Principal tags
- From the IdP via **session tags** (SAML attribute `https://aws.amazon.com/SAML/Attributes/PrincipalTag:project`), so HR/IdP data drives access.
- Mark as transitive only when role chaining needs them.

## Protect the tags (critical)
Anyone who can change a resource's tag or their own principal tag can grant themselves access.
- Deny `ec2:CreateTags`/`DeleteTags` (and service equivalents) on the controlling keys unless `aws:ResourceTag/project` already equals the principal's project, or unless the principal is an admin pipeline.
- Deny `iam:TagRole`/`TagUser` for non-admins; SCP to protect tag keys org-wide.

## Limits
- Not all services/actions support `aws:ResourceTag` or `aws:RequestTag` - check the services-that-work-with-IAM table; use resource ARNs for the rest.
- Tag-on-create must be allowed in the same call (RunInstances with TagSpecifications).

## Checked

2026-10-28: confirmed on the session tags page: the SAML attribute name `https://aws.amazon.com/SAML/Attributes/PrincipalTag:{TagKey}`, session tags can be set transitive for role chaining, `aws:PrincipalTag`; ABAC via `aws:ResourceTag` conditions on the IAM pages. Removed: IAM Identity Center attribute claim, the "ABAC column" wording and the tag policies line (not confirmed).

Method: documentation only; no commands were run.

## Verify
- [ ] Principal with project=alpha can stop alpha instances, gets AccessDenied on beta.
- [ ] Principal cannot retag a beta instance to alpha (deny tested with IAM policy simulator and live).
