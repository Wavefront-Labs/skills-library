---
id: computing-software.cloud-infrastructure-engineering.aws.organizations-declarative-policies
name: organizations-declarative-policies
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, aws-organizations, declarative-policies, declarative-policy, declarative-policy-ec2, service-baseline, image-block-public-access, snapshot-block-public-access, vpc-block-public-access, imds-defaults, serial-console, allowed-images, account-status-report]
level: advanced
status: docs-checked
description: "Lock EC2/VPC/EBS configuration baselines org-wide with Organizations declarative policies: syntax, attributes, account status reports, rollout and how they differ from SCPs."
sources: ["https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_policies_declarative.html", "https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_policies_ec2_syntax.html", "https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_policies_ec2_status-report.html", "https://docs.aws.amazon.com/organizations/latest/userguide/policy-operators.html", "https://aws.amazon.com/blogs/aws/simplify-governance-with-declarative-policies/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Organizations declarative policies

**Goal:** settings such as "no public AMIs", "no public EBS snapshots", "IMDSv2 by default"
and "VPC block public access" are fixed at the OU level as *service configuration*, so they
hold even for new APIs and new features, and account administrators cannot change the enforced value.

## 1. Declarative policy vs SCP
| | SCP | Declarative policy (`DECLARATIVE_POLICY_EC2`) |
|---|---|---|
| Works on | API calls (deny actions) | The service's account-level configuration |
| Coverage of new APIs | Must be updated for each new action | Automatic: the setting itself is enforced |
| Error the user sees | `AccessDenied` explicit deny in SCP | Configurable custom message + the change is refused |
| Scope | Org/OU/account | Org/OU/account |
Use both: declarative for the baseline, SCPs for "who may call what".

## 2. Enable and write
```bash
aws organizations enable-policy-type --root-id r-xxxx --policy-type DECLARATIVE_POLICY_EC2
```
Policy body (management account or delegated admin for Organizations policies):
```json
{
 "ec2_attributes": {
  "image_block_public_access":    {"state": {"@@assign": "block_new_sharing"}},
  "snapshot_block_public_access": {"state": {"@@assign": "block_all_sharing"}},
  "instance_metadata_defaults": {
     "http_tokens": {"@@assign": "required"},
     "http_put_response_hop_limit": {"@@assign": "2"},
     "http_endpoint": {"@@assign": "enabled"},
     "instance_metadata_tags": {"@@assign": "enabled"},
     "http_tokens_enforced": {"@@assign": "enabled"}},
  "serial_console_access": {"status": {"@@assign": "disabled"}},
  "vpc_block_public_access": {"internet_gateway_block": {"mode": {"@@assign": "block_ingress"},
                              "exclusions_allowed": {"@@assign": "enabled"}}},
  "exception_message": {"@@assign": "Blocked by org baseline. Ask #platform for an exception."}
 }
}
```
```bash
aws organizations create-policy --type DECLARATIVE_POLICY_EC2 --name ec2-baseline \
  --content file://ec2-baseline.json --description "EC2/EBS/VPC baseline"
aws organizations attach-policy --policy-id p-xxxx --target-id ou-xxxx-sandbox   # start small
```
The EC2 policy syntax page also documents `allowed_images_settings` (with an `audit_mode`) and
`vpc_encryption_control`. Enabling IMDSv2 enforcement while IMDSv1 is still allowed causes launch
failures unless IMDSv1 is disabled by launch parameters or AMI defaults, so audit IMDSv1 use first.
Attribute names and allowed values evolve; confirm against the syntax page before writing.

## 3. Account status report first
Before attaching to production OUs, see which accounts and Regions currently differ:
```bash
aws ec2 start-declarative-policies-report --s3-bucket org-reports-<ACCOUNT_ID> \
  --s3-prefix declarative/ --target-id r-xxxx       # root, OU or account
aws ec2 describe-declarative-policies-reports
```
The report is asynchronous and can take several hours. It shows, per attribute and Region, how many
accounts match and how many do not (`numberOfMatchedAccounts`, `numberOfUnmatchedAccounts`) and the
most frequent value. Prerequisites: call it from the management account or an EC2 delegated administrator,
enable trusted access for EC2, and use an S3 bucket in the same Region with the documented bucket policy;
only one report runs at a time. Fix intentional outliers (e.g. a public AMI publishing account) by placing them in an OU with an override
(`@@assign` lower down) rather than leaving them out.

## 4. Rollout
1. Report → 2. Attach to Sandbox OU → 3. Watch tickets for a week → 4. Workloads OU →
5. Root. Use inheritance operators (`@@assign`, `@@append`, `@@remove`, and
`@@operators_allowed_for_child_policies` to limit what child policies may do) to stop OUs below
from overriding.
6. Document the exception path; the `exception_message` is what engineers see, so make it
actionable.

## Gotchas
- The instance metadata attribute controls IMDS defaults and IMDSv2 enforcement for new launches.
  Pair with a Config rule to find existing instances that differ.
- VPC BPA `block_bidirectional` blocks all traffic to and from internet gateways except excluded VPCs
  and subnets; start with `block_ingress` and `exclusions_allowed`.
- Account administrators cannot change a declaratively-enforced setting (the related API calls
  such as `ModifyVpcBlockPublicAccessOptions` fail), and detaching the policy rolls the attribute back to its
  previous state. Make sure break-glass procedures are written down.

## Verify
- [ ] `describe-effective-policy --policy-type DECLARATIVE_POLICY_EC2 --target-id <ACCOUNT_ID>` shows the merged policy.
- [ ] In a target account, `aws ec2 enable-image-block-public-access`/disable attempts are refused with the custom message.
- [ ] `aws ec2 get-instance-metadata-defaults` in a target Region shows `HttpTokens: required` managed by the org.
- [ ] A new status report shows all attached accounts compliant.

## Checked

Checked 2026-10-27 against the AWS Organizations User Guide pages on declarative policies, EC2 policy syntax and examples, the account status report for EC2 policies, and policy operators, plus the botocore organizations and ec2 models:
- `DECLARATIVE_POLICY_EC2` is a valid policy type; `ec2_attributes` and the attribute values shown (`block_new_sharing`, `block_all_sharing`, `required`, `block_ingress`, serial console `status`, `exception_message`) match the syntax page, which also lists `http_tokens_enforced`, `allowed_images_settings` and `vpc_encryption_control`.
- Declarative policies are enforced in the service control plane, apply to the root, OUs or accounts, and roll back on detach.
- Status report prerequisites, asynchronous generation and the matched/unmatched account counts; `start-declarative-policies-report` takes `--s3-bucket`, `--s3-prefix` and `--target-id`; `describe-declarative-policies-reports` exists.
- Inheritance operators `@@assign`, `@@append`, `@@remove` and `@@operators_allowed_for_child_policies`.
Removed: the claims that enforcement is per Region and that the root user is specifically blocked, and the CSV description, which the pages do not state. The commands were not run.

Method: documentation only; no commands were run.
