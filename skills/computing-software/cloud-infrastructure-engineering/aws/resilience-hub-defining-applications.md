---
id: computing-software.cloud-infrastructure-engineering.aws.resilience-hub-defining-applications
name: resilience-hub-defining-applications
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, resilience-hub, resilience-hub-application, app-components, resiliency-policy, rto-rpo, resilience-assessment]
level: practitioner
status: docs-checked
description: "Define applications in AWS Resilience Hub from CloudFormation, Terraform state, Resource Groups or EKS, group app components, attach an RTO/RPO policy and assess."
sources: ["https://docs.aws.amazon.com/resilience-hub/latest/userguide/describe-applicationlication.html", "https://docs.aws.amazon.com/resilience-hub/latest/userguide/discover-structure.html", "https://docs.aws.amazon.com/resilience-hub/latest/userguide/AppComponent.grouping.html", "https://docs.aws.amazon.com/resilience-hub/latest/userguide/setup-resiliency-policy.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Defining applications in Resilience Hub

## Input sources
| Source | Notes |
|---|---|
| CloudFormation stacks | stacks can be from other accounts or Regions (add by stack ARN) |
| AWS Resource Groups | groups can be from other accounts or Regions (add by group ARN) |
| Terraform state files | in S3; state file version 0.12 or later; 4 MB limit per file |
| Amazon EKS clusters | choose clusters and add the namespaces to assess; the names must match exactly; extra IAM roles are needed |

```bash
aws resiliencehub create-app --name orders --assessment-schedule Daily \
  --policy-arn "$POLICY_ARN" --permission-model '{"type":"RoleBased","invokerRoleName":"<INVOKER_ROLE>"}'
aws resiliencehub import-resources-to-draft-app-version --app-arn "$APP" \
  --source-arns <CLOUDFORMATION_STACK_ARN> \
  --terraform-sources s3StateFileUrl=s3://<BUCKET>/<KEY>.tfstate
aws resiliencehub publish-app-version --app-arn "$APP"
```
Then start an assessment of the published version (`aws resiliencehub start-app-assessment`).

## App components
- Resources are grouped into AppComponents; the console offers grouping recommendations, and you can group manually.
- Make each component a logical tier; assessments and recommendations are reported per component.

## Resiliency policy
RTO and RPO targets are set for infrastructure and Availability Zone, plus an optional Region target for
multi-Region applications. Entering 0 gives a near-zero estimate and the status `Policy breached`, so use real targets.
You can pick an existing policy or define your own.

## Verify
- [ ] The published app version lists all expected resources in sensible components.
- [ ] An assessment has run and breached items have owners.

## Checked
2026-10-28. Confirmed in the Resilience Hub User Guide pages in `sources` (adding resources, AppComponent grouping, setting RTO and RPO) and the botocore model (`CreateApp`: `assessmentSchedule` Disabled/Daily, `permissionModel`, `policyArn`); commands checked with check_commands.
Removed (not confirmed on fetched pages): AppRegistry as an input source, the "Application" disruption type, tier names, assessment output and permissions sections, the `--app-version` value, and the example ARNs and bucket names (now placeholders).
Method: documentation only; no commands were run.
