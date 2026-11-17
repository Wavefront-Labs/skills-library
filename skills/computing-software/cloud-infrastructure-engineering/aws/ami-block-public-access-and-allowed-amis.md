---
id: computing-software.cloud-infrastructure-engineering.aws.ami-block-public-access-and-allowed-amis
name: ami-block-public-access-and-allowed-amis
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, ami, block-public-ami, allowed-amis, image-criteria, declarative-policies, ebs-snapshot-block-public-access]
level: practitioner
status: docs-checked
description: "Stop AMI leaks and untrusted images: block public sharing of AMIs and EBS snapshots, restrict launches to Allowed AMIs criteria in audit then enabled mode, enforce org-wide."
sources: ["https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/block-public-access-to-amis.html", "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-allowed-amis.html", "https://docs.aws.amazon.com/ebs/latest/userguide/block-public-access-snapshots.html", "https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_policies_declarative_syntax.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AMI block public access and Allowed AMIs

Two different controls:
- **Block public access (BPA) for AMIs** stops your AMIs being made public (data leak risk).
- **Allowed AMIs** restricts which public or shared AMIs principals in the account can discover and launch
  (supply-chain risk). It never restricts AMIs owned by your own account.

## 1. Block public access for AMIs (per Region)
```bash
aws ec2 enable-image-block-public-access --image-block-public-access-state block-new-sharing
aws ec2 get-image-block-public-access-state
```
- `block-new-sharing` is the only state; it blocks new public sharing, and AMIs already public stay public. Find and fix them:
  `aws ec2 describe-images --owners self --filters Name=is-public,Values=true`
  then `modify-image-attribute --launch-permission 'Remove=[{Group=all}]'`.
- Defaults: new accounts enabled; existing accounts with no public AMIs enabled (but disabled if the account had a public AMI on or after 15 July 2023, even if since made private); existing accounts with public AMIs disabled.
- The setting is per account and per Region; a declarative policy applies it across Regions and accounts, and then you cannot change it in the account. You can limit who may enable or disable it with IAM.
- EBS snapshots have a separate Regional setting:
  `aws ec2 enable-snapshot-block-public-access --state block-all-sharing`
  (states: `block-all-sharing`, `block-new-sharing`, `unblocked`; see the EBS page for exactly what each does to existing public snapshots).

## 2. Allowed AMIs
Account-level, per Region. Up to 10 criteria; each criterion can hold up to 200 `ImageProviders`, 50 `ImageNames` and 50 `MarketplaceProductCodes`. Values within one parameter are OR'ed; a criterion's parameters are combined (AND), and an AMI is allowed if it matches any criterion. Fields: `ImageProviders` (`amazon`, `aws-marketplace`, `aws-backup-vault` (needed if you use AWS Backup logically air-gapped vaults), `none` (only your own AMIs; no other criteria allowed), account IDs), `ImageNames` (exact or `?`/`*` wildcards), `MarketplaceProductCodes`, `CreationDateCondition`, `DeprecationTimeCondition`.
```bash
aws ec2 replace-image-criteria-in-allowed-images-settings --image-criteria '[
  {"ImageProviders": ["amazon", "<GOLDEN_IMAGE_ACCOUNT_ID>"]},
  {"ImageProviders": ["aws-marketplace"], "MarketplaceProductCodes": ["<PRODUCT_CODE>"]}]'
aws ec2 enable-allowed-images-settings --allowed-images-settings-state audit-mode
aws ec2 get-allowed-images-settings
```
- States: `enabled`, `disabled`, `audit-mode`. In `audit-mode` nothing is blocked and `describe-images` returns `"ImageAllowed": true|false`.
- Find instances launched from AMIs that would not be allowed: the AWS Config rule `ec2-instance-launched-with-allowed-ami` (works in enabled or audit mode) or `describe-instance-image-metadata`.
- With `enabled`, instances can only be launched from allowed AMIs.
- Pair `ImageNames` with `ImageProviders` (names alone may not identify one AMI). Avoid very short `CreationDateCondition` windows: launches fail if AMIs are not refreshed within the window.
- For managed services such as ECS, EKS and Lambda Managed Instances, allow the `amazon` alias because they rely on Amazon-published AMIs; watch EMR, EKS and Elastic Beanstalk launches after enabling.

## 3. Organization-wide enforcement
Use an Organizations **declarative policy** for EC2 so member accounts cannot change the settings:
```json
{"ec2_attributes": {
   "image_block_public_access": {"state": {"@@assign": "block_new_sharing"}},
   "allowed_images_settings": {"state": {"@@assign": "audit_mode"},
     "image_criteria": {"criteria_1": {"allowed_image_providers": {"@@append": ["amazon", "<GOLDEN_IMAGE_ACCOUNT_ID>"]}}}}}}
```
The declarative policy syntax page documents `image_block_public_access`, `allowed_images_settings` and `image_criteria`; take the snapshot setting's key and values from the same page. `aws ec2 start-declarative-policies-report` produces an account status report before you enforce.

## 4. Rollout
1. Enable AMI and snapshot BPA everywhere.
2. Allowed AMIs in audit mode first; fix pipelines using community AMIs.
3. Switch to enabled per OU starting with sandbox; test third-party AMIs in a Region where it is not yet enabled.
4. Document how teams request a new provider or product.

## Verify
- [ ] `get-image-block-public-access-state` and `get-snapshot-block-public-access-state` show blocking in all used Regions.
- [ ] `describe-images --owners self --filters Name=is-public,Values=true` returns nothing.
- [ ] In enabled mode, launching a non-allowed public AMI fails; launching the golden AMI works.

## Checked
2026-10-28. Confirmed on the block-public-access-to-amis, ec2-allowed-amis, block-public-access-snapshots and declarative-syntax pages and the ec2 botocore model: defaults table and July 2023 rule, criteria limits and aliases, states, ImageAllowed, Config rule, managed-service advice, declarative keys (`image_block_public_access`, `allowed_images_settings`, `image_criteria`, `@@append`), snapshot state enum, `StartDeclarativePoliciesReport` and `DescribeInstanceImageMetadata` operations. Removed as unconfirmed: the `NotAuthorized` error text, running instances unaffected, SSM public parameter remark, Bottlerocket remark, the snapshot declarative-policy key, "weeks" of audit, a made-up account ID.
Method: documentation only; no commands were run.
