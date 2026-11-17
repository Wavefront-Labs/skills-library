---
id: computing-software.cloud-infrastructure-engineering.aws.config-organization-rules-and-conformance-packs
name: config-organization-rules-and-conformance-packs
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, aws-config, organization-config-rules, org-conformance-pack, delegated-administrator, compliance-as-code, config-aggregator]
level: practitioner
status: docs-checked
description: "Deploy AWS Config rules and conformance packs to every account from a delegated admin, exclude accounts, track per-account deployment status and aggregate results."
sources: ["https://docs.aws.amazon.com/config/latest/developerguide/config-rule-multi-account-deployment.html", "https://docs.aws.amazon.com/config/latest/developerguide/conformance-pack-organization-apis.html", "https://docs.aws.amazon.com/config/latest/APIReference/API_PutOrganizationConfigRule.html", "https://docs.aws.amazon.com/config/latest/APIReference/API_PutOrganizationConformancePack.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Organization Config rules and conformance packs

**Goal:** one place (a Security Tooling delegated admin) pushes compliance rules to every
account and region, new accounts receive them automatically, and members cannot modify them.

## 1. Prerequisites
- AWS Config recording on in every member account and Region before you call the organization
  APIs. If no recorder is available when an account joins, deployment is retried for only 7 hours.
- Trusted access and delegated admin:
```bash
aws organizations enable-aws-service-access --service-principal config-multiaccountsetup.amazonaws.com
aws organizations register-delegated-administrator --account-id 222233334444 \
  --service-principal config-multiaccountsetup.amazonaws.com
```

## 2. Organization managed rule
```bash
aws configservice put-organization-config-rule \
  --organization-config-rule-name org-s3-bucket-ssl-requests-only \
  --organization-managed-rule-metadata '{"RuleIdentifier":"S3_BUCKET_SSL_REQUESTS_ONLY",
     "ResourceTypesScope":["AWS::S3::Bucket"]}' \
  --excluded-accounts 999988887777
```
Custom Lambda org rules: the Lambda function lives in the management or delegated
administrator account, and an IAM role in the managed account must be assumable by that
function. Guard-based custom policy rules (`OrganizationCustomPolicyRuleMetadata`) use a
policy-as-code definition instead of a Lambda function.

## 3. Organization conformance pack
```bash
aws configservice put-organization-conformance-pack \
  --organization-conformance-pack-name org-fsbp-subset \
  --template-s3-uri s3://org-config-packs/operational-best-practices-for-cis.yaml \
  --delivery-s3-bucket awsconfigconforms-org-results \
  --excluded-accounts 999988887777
```
- Template from an S3 object (`--template-s3-uri`, an `s3://` URI) or inline (`--template-body`).
- `--delivery-s3-bucket` is optional; if used, the bucket name must be prefixed with `awsconfigconforms`.
- Parameters via `--conformance-pack-input-parameters`.

## 4. Status and troubleshooting
```bash
aws configservice get-organization-config-rule-detailed-status \
  --organization-config-rule-name org-s3-bucket-ssl-requests-only \
  --filters MemberAccountRuleStatus=CREATE_FAILED
aws configservice get-organization-conformance-pack-detailed-status \
  --organization-conformance-pack-name org-fsbp-subset
```
Common failure: no recorder in a member account or Region (see section 1). The detailed status
lists the state of each member account. Member accounts cannot modify the underlying rules.

## 5. Results in one view
Aggregator in the admin account:
```bash
aws configservice put-configuration-aggregator --configuration-aggregator-name org \
  --organization-aggregation-source RoleArn=arn:aws:iam::222233334444:role/ConfigAggregator,AllAwsRegions=true
aws configservice get-aggregate-compliance-details-by-config-rule ...
```
Advanced query across the org: `aws configservice select-aggregate-resource-config
--configuration-aggregator-name org --expression "<SQL>"` (expression up to 4096 characters;
see the Config advanced query documentation for the syntax).

## Gotchas
- Org rules are regional: repeat `put-organization-config-rule` per region (script it).
- Deleting an org rule deletes it and its evaluation results from all member accounts.
- A delegated administrator cannot see organization rules deployed from the management account, and vice versa.

## Verify
- [ ] Detailed status shows `CREATE_SUCCESSFUL` for every member and region.
- [ ] A newly vended account receives the rules within minutes.
- [ ] Aggregator compliance view shows all accounts; a deliberately non-compliant test resource appears as NON_COMPLIANT.

## Checked

Checked 2026-10-28 against the AWS Config Developer Guide (organization rules and conformance packs), the PutOrganizationConfigRule and PutOrganizationConformancePack API pages, and the AWS Config service model (botocore).
- Confirmed: service principal `config-multiaccountsetup.amazonaws.com` for the delegated administrator, region-specific deployment, 7-hour recorder retry, exclude-accounts, `OrganizationManagedRuleMetadata` and `OrganizationCustomPolicyRuleMetadata` (Guard), template S3 URI or body, `awsconfigconforms` bucket prefix, input parameters, detailed-status filter and its `CREATE_SUCCESSFUL`/`CREATE_FAILED` values, organization aggregation source, `SelectAggregateResourceConfig` parameters.
- Removed: the `config.amazonaws.com` trusted-access and Lambda invoke-permission steps, the `awslabs/aws-config-rules` template pointer, the `OrgConfigRule-` prefix, the member SCP cause, the cost-per-evaluation and Security Hub remarks, and the example SQL expression.

Method: documentation only; no commands were run.
