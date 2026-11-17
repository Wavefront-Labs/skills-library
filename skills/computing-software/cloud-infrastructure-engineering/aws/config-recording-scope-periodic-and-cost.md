---
id: computing-software.cloud-infrastructure-engineering.aws.config-recording-scope-periodic-and-cost
name: config-recording-scope-periodic-and-cost
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, aws-config, periodic-recording, config-cost, configuration-recorder, recording-group]
level: advanced
status: docs-checked
description: "Control AWS Config cost by scoping the recorder: exclude ephemeral resource types, use daily recording for high-churn types, and record global IAM types once."
sources: ["https://docs.aws.amazon.com/config/latest/developerguide/select-resources.html", "https://docs.aws.amazon.com/config/latest/developerguide/stop-start-recorder.html", "https://aws.amazon.com/config/pricing/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Config recording scope, periodic recording and cost

Per the pricing page, Config charges by the number of configuration items (CIs) recorded, the number of active rule
evaluations and the number of conformance pack evaluations; see that page for rates (continuous and periodic CIs are
priced differently). Ephemeral workloads such as EC2 Spot Instances, EMR jobs and Auto Scaling generate extra CIs and
evaluations as resources are created and deleted.

## 1. Scope the recorder
- A customer managed recorder records all supported resource types by default, excluding the global IAM types
  (`AWS::IAM::Group`, `Policy`, `Role`, `User`). There is one customer managed recorder per account per Region.
- To avoid ephemeral-workload churn the page suggests excluding those resource types from the customer managed recorder,
  or running such workloads in a separate account with Config turned off.
- A resource type that is not recorded still produces create and delete CIs (`ResourceNotRecorded`,
  `ResourceDeletedNotRecorded`) at no cost, sent at the periodic baselining rather than immediately.

## 2. Exclude, or record daily
```bash
aws configservice put-configuration-recorder --configuration-recorder '{
  "name":"default","roleARN":"arn:aws:iam::<ACCOUNT_ID>:role/<CONFIG_ROLE>",
  "recordingGroup":{"allSupported":false,
    "exclusionByResourceTypes":{"resourceTypes":["AWS::EC2::NetworkInterface"]},
    "recordingStrategy":{"useOnly":"EXCLUSION_BY_RESOURCE_TYPES"}},
  "recordingMode":{"recordingFrequency":"CONTINUOUS",
    "recordingModeOverrides":[{"description":"daily for fleet churn","resourceTypes":["AWS::EC2::Instance"],"recordingFrequency":"DAILY"}]}}'
aws configservice describe-configuration-recorders
```
- Strategies in the API model: `ALL_SUPPORTED_RESOURCE_TYPES`, `INCLUSION_BY_RESOURCE_TYPES`,
  `EXCLUSION_BY_RESOURCE_TYPES`. The model allows at most one entry in `recordingModeOverrides`.
- Daily recording gives one CI for the most recent state over the last 24 hours, only if it differs from the previous CI;
  continuous records each change as it happens (page).
- Firewall Manager depends on continuous recording; the page recommends Continuous if you use it.
- When a `PAID`-scope service-linked recorder also records a type you set to daily, the higher frequency wins, so that
  type is recorded and billed continuously, once per CI.

## 3. Global resources
- Global IAM types (users, groups, roles, customer managed policies) can be recorded only in Regions Config supported
  before February 2022. To avoid duplicate CIs, record them in one such Region.
- If you do not record them, the page recommends not enabling periodic IAM rules such as `iam-password-policy`,
  `iam-user-mfa-enabled` and `root-account-mfa-enabled` (full list on the page), and deploying rules that cover them to one Region.
- Global types onboarded after February 2022 (CloudFront, Route 53, WAF, Global Accelerator, ECR Public) record only in their
  home Region. `AWS::RDS::GlobalCluster` records in every Region where the recorder is enabled; use an exclusion or
  inclusion strategy if you do not want that.

## Gotchas
- Turning the recorder off stops tracking deletions, so stale evaluation results can persist for deleted resources.
- Service-linked recorders cannot be changed directly; change them through the linked service.

## Verify
- [ ] `describe-configuration-recorders` shows the intended `recordingGroup` and `recordingMode`.
- [ ] CI volume and the Config line on your bill fall after the change (see the pricing page for the billing basis).

## Checked
Date: 2026-11-07. Read in full: select-resources (Recording AWS Resources with AWS Config: considerations, global
and regional resources, recording frequency, non-recorded resources); stop-start-recorder (considerations for customer
managed and service-linked recorders, drift detection; the start/stop/frequency subtopics are separate pages not opened);
the pricing page's introduction and example 1 (rates not copied). The put-configuration-recorder JSON was checked against the botocore
model (field names, enums, override limit); the model does not state that excluding a type has any rule effect.
Removed because no page read states them: the Cost Explorer usage type, the advanced-query SQL, the named "typical
offenders" list beyond the page's ephemeral examples, "short-lived resources may never be recorded", the Control Tower
recorder-management claim, "excluding a type breaks conformance-pack rules", and the CI-per-day Verify timings. The
page's exact CLI text for excluding resources was not read.
Method: documentation only; no commands were run.
