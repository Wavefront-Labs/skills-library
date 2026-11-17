---
id: computing-software.cybersecurity-defensive.cloud-security.aws-resource-control-policies
name: aws-resource-control-policies
category: computing-software
field: cybersecurity-defensive
product: cloud-security
tags: [iam-least-privilege, resource-control-policies, rcp, data-perimeter, aws-organizations, scp]
level: advanced
status: docs-checked
description: "Use AWS Resource Control Policies to cap what can be done to org resources: what RCPs do and do not cover, rollout testing, and the data-perimeter sample repo."
sources: ["https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_policies_rcps.html", "https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_policies_rcps_examples.html", "https://github.com/aws-samples/data-perimeter-policy-examples"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AWS Resource Control Policies

- **SCPs** limit permissions of IAM principals in member accounts. **RCPs** restrict principals (notably external ones) making requests to access resources in member accounts.
- An RCP never grants permission. It sets the maximum available permissions for resources; effective permissions are the intersection of SCP/RCP limits and the identity-based and resource-based policies that actually grant access.
- Requires an organisation with all features enabled (not consolidated-billing only).

## Scope
- RCPs affect only resources in member accounts of the organisation that attached them (including member accounts that are delegated administrators). They do not affect the management account's resources, and do not affect resources in accounts outside the org.
- An RCP applies to any principal accessing the resource, in or out of the org, including root users.
- Not restricted: service-linked roles (and AWS services assuming them), AWS managed KMS keys, and `kms:RetireGrant`.
- Supported services are a long, growing list (documented with IAM prefixes). It includes S3, STS, KMS, SQS, Secrets Manager, DynamoDB, ECR, CloudWatch Logs, EventBridge, OpenSearch, Cognito, CodeArtifact and many more. Check the page for the current list before relying on a service.

## Default and evaluation
`RCPFullAWSAccess` is attached automatically to the root, every OU and every account when RCPs are enabled; it lets everything pass RCP evaluation, so you restrict with Deny statements. A resource has only the permissions permitted by every level above it.

## Rollout
- Do not attach to the org root untested. Start with test accounts, move to lower OUs, then up the hierarchy; review CloudTrail for AccessDenied errors.
- Before writing denies, review IAM Access Analyzer external access findings to see which resources are public or shared externally.
- Deny-based RCPs can block AWS service use unless you add the needed exceptions; the AWS example policies are not official recommendations to apply as-is.

## Data perimeter reference
The `aws-samples/data-perimeter-policy-examples` repo holds sample SCPs, RCPs, VPC endpoint policies and resource-based policies for identity, resource and network perimeters. RCP samples cover identity and network perimeters and use `aws:PrincipalAccount`. Exceptions are tag-driven: `dp:exclude` (all controls), `dp:exclude:identity`, `dp:exclude:network`, `dp:include:network`, `dp:exclude:resource` (and per-service variants). Governance SCP/RCP samples protect those tags from unauthorised change.

## Illustrative identity-perimeter deny (authored here, not copied from the pages)
```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Sid": "EnforceOrgIdentities",
    "Effect": "Deny",
    "Principal": "*",
    "Action": ["s3:*", "sqs:*", "kms:*", "secretsmanager:*", "sts:AssumeRole"],
    "Resource": "*",
    "Condition": {
      "StringNotEqualsIfExists": {"aws:PrincipalOrgID": "o-exampleorgid"},
      "BoolIfExists": {"aws:PrincipalIsAWSService": "false"}
    }
  }]
}
```
Test it against the repo's maintained versions before use; AWS service principals and legitimate third parties need carve-outs.

## Verify
From an account outside the org with a bucket policy that grants it access, access fails with an explicit deny; in-org access and tagged exceptions still work.

## Checked
Method: 2026-11-08 read the AWS Organizations RCP and RCP examples pages and the data-perimeter-policy-examples README in full. Rewrote scope, default policy and rollout to the pages; replaced the old short service list with a pointer to the long documented list; removed "since Nov 2024", the 5-RCP and 5120-character limits, and the confused-deputy aws:SourceOrgID claim (not stated on the cited pages). The JSON deny is labelled illustrative and unverified against the pages; other claims unchanged.
