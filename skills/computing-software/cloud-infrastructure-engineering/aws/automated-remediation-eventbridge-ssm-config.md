---
id: computing-software.cloud-infrastructure-engineering.aws.automated-remediation-eventbridge-ssm-config
name: automated-remediation-eventbridge-ssm-config
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, auto-remediation, automated-remediation, remediation, aws-config, config-rules, conformance-packs, ssm-automation, automation-runbooks, eventbridge, security-hub-automation, guardduty-response, self-healing, event-driven-ops, config-remediation, opsitems, incident-manager, remediation-safety, automatic-remediation, remediation-retry]
level: practitioner
status: draft
description: "Build self-healing AWS controls: Config rules with SSM Automation remediation, EventBridge rules on CloudTrail/GuardDuty/Health events, and the guardrails that stop remediation causing an outage."
sources: ["AWS Config Developer Guide - Remediating noncompliant resources with AWS Config rules", "AWS Systems Manager User Guide - Automation runbook reference (AWS-* documents)", "Amazon EventBridge User Guide - Events from AWS services", "AWS Security Hub User Guide - Automation rules and automated response"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Automated remediation — fix the known-bad in seconds, with a human for the unknown

**Goal:** misconfigurations and known failure modes are detected by Config/EventBridge and
fixed by an SSM Automation runbook automatically, with rate limits, exclusions and an
audit trail, while anything ambiguous becomes an OpsItem for a person.

## 1. The three triggers
| Trigger | Fires on | Best for |
|---|---|---|
| **AWS Config rule** (managed/custom) | Resource becomes NON_COMPLIANT (config change or periodic) | Posture drift: public S3, open SG, unencrypted EBS, missing tags |
| **EventBridge rule** on service events / CloudTrail API calls | Near real time (seconds) | Reacting to an action (someone called `AuthorizeSecurityGroupIngress`), GuardDuty findings, Health events, alarms |
| **Security Hub automation rule** | Finding ingested/updated | Suppressing/enriching findings, routing; pair with EventBridge for action |

## 2. Config rule + remediation
```bash
aws configservice put-config-rule --config-rule '{"ConfigRuleName":"s3-public-read","Source":{"Owner":"AWS","SourceIdentifier":"S3_BUCKET_PUBLIC_READ_PROHIBITED"}}'
aws configservice put-remediation-configurations --remediation-configurations '[{
  "ConfigRuleName":"s3-public-read","TargetType":"SSM_DOCUMENT","TargetId":"AWS-DisableS3BucketPublicReadWrite",
  "Automatic":true,"MaximumAutomaticAttempts":3,"RetryAttemptSeconds":60,
  "Parameters":{"AutomationAssumeRole":{"StaticValue":{"Values":["arn:aws:iam::<acct>:role/ConfigRemediation"]}},
                "S3BucketName":{"ResourceValue":{"Value":"RESOURCE_ID"}}}}]'
```
- `ResourceValue: RESOURCE_ID` passes the non-compliant resource id into the runbook.
- Managed runbooks that exist for the common cases: `AWS-DisableS3BucketPublicReadWrite`,
  `AWS-EnableS3BucketEncryption`, `AWS-DisablePublicAccessForSecurityGroup`,
  `AWS-EnableCloudTrail`, `AWS-ConfigureS3BucketLogging`, `AWS-EnableEbsEncryptionByDefault`,
  `AWSConfigRemediation-*` family (RDS public access, EBS snapshot public, IAM key rotation…).
- **Conformance packs** (`Operational-Best-Practices-for-*`, CIS) bundle rules + remediation
  across an org; deploy via Organizations conformance packs.
- Exclusions: a resource tag like `remediation=exempt` checked by a *custom* rule
  (Lambda or Guard policy) or by the runbook's first step — managed rules do not read your tags.

## 3. EventBridge → SSM Automation / Lambda
```json
{"source":["aws.ec2"],"detail-type":["AWS API Call via CloudTrail"],
 "detail":{"eventName":["AuthorizeSecurityGroupIngress"],
           "requestParameters":{"ipPermissions":{"items":{"ipRanges":{"items":{"cidrIp":["0.0.0.0/0"]}}}}}}}
```
Target: SSM Automation (`AWS-DisablePublicAccessForSecurityGroup` with input transformer
mapping `$.detail.requestParameters.groupId` → `GroupId`) or a Lambda that revokes the rule,
tags the SG `remediated-by=auto`, and posts to Slack with the caller's ARN (`detail.userIdentity`).
- CloudTrail-based events arrive ~minutes after the API call (management events delivered to
  EventBridge); for seconds-level reaction use service-native events (GuardDuty, Health,
  CloudWatch alarm state change `aws.cloudwatch`).
- **GuardDuty** findings: `source: aws.guardduty`, filter `detail.severity >= 7` and
  `detail.type` prefix (`UnauthorizedAccess:EC2/…`) → runbook that isolates the instance
  (swap to a quarantine SG, snapshot volumes, tag) — the classic incident-response automation.
- **CloudWatch alarm** state change → runbook `AWS-RestartEC2Instance` / scale action / failover.
- Give rules a **DLQ** (SQS) and retries (`RetryPolicy`); failed invocations otherwise vanish.

## 4. Writing a safe runbook
```yaml
schemaVersion: '0.3'
assumeRole: '{{ AutomationAssumeRole }}'
parameters: { InstanceId: {type: String}, AutomationAssumeRole: {type: String} }
mainSteps:
  - name: checkExempt
    action: aws:executeAwsApi
    inputs: { Service: ec2, Api: DescribeTags, Filters: [{Name: resource-id, Values: ['{{ InstanceId }}']}] }
    outputs: [{ Name: tags, Selector: $.Tags, Type: MapList }]
  - name: branch
    action: aws:branch
    inputs: { Choices: [{ NextStep: done, Variable: '{{ checkExempt.tags }}', Contains: 'remediation=exempt' }], Default: fix }
  - name: fix
    action: aws:executeAwsApi
    inputs: { Service: ec2, Api: ModifyInstanceMetadataOptions, InstanceId: '{{ InstanceId }}', HttpTokens: required }
  - name: done
    action: aws:sleep
    inputs: { Duration: PT1S }
```
- Steps: `aws:executeAwsApi`, `aws:executeScript` (Python/PowerShell), `aws:runCommand`,
  `aws:approve` (SNS + IAM approvers — use for destructive actions), `aws:waitForAwsResourceProperty`,
  `aws:branch`, `aws:assertAwsResourceProperty`.
- Scoped `AutomationAssumeRole` per runbook (least privilege), `onFailure: Abort`, idempotent
  steps, and a final step that writes a tag/OpsItem with what changed.
- Rate control: `start-automation-execution --target-parameter-name InstanceId --targets …
  --max-concurrency 5 --max-errors 2` for fleet-wide runs; for Config, `MaximumAutomaticAttempts`
  prevents loops when the fix does not stick.

## 5. Guardrails before you turn on `Automatic: true`
1. Run in **manual** mode for two weeks; review what *would* have fired.
2. Exempt by tag; never remediate in accounts/OUs marked break-glass or data-migration.
3. Alert on every remediation (EventBridge `aws.ssm` `EC2 Automation Step Status-change Notification` /
   `aws.config` `Config Rules Remediation…`) — silence is not success.
4. Budget the blast radius: one runbook per rule, no "fix everything" scripts; a kill switch
   (disable the rule/remediation) documented in the runbook of the on-call.
5. Route non-actionable findings to **OpsCenter OpsItems** (`aws:createOpsItem`) or Incident
   Manager instead of guessing.

## Gotchas
- Config remediation needs the rule to be evaluated *again* to clear — compliance lags the fix by minutes.
- Managed remediation documents assume parameters named exactly as documented; a typo = silent `Failed` with no finding.
- Remediation of an SG rule a deployment pipeline just created = fight with the pipeline; exempt IaC roles via the event's `userIdentity`.
- EventBridge `detail` matching is exact on arrays (`cidrIp` must match `0.0.0.0/0`, not `::/0`) — add both.
- Config costs per evaluation; periodic rules at 1 h across thousands of resources add up — use change-triggered where possible.
- Unconfirmed: current list of `AWSConfigRemediation-*` runbooks — list with `aws ssm list-documents --filters Key=Owner,Values=Amazon Key=Name,Values=AWSConfigRemediation`.

## Verify
- [ ] Open an SG to `0.0.0.0/0:22` in a sandbox: rule revoked within 5 min, Slack message names the caller, SG tagged.
- [ ] The same SG tagged `remediation=exempt` is left alone and an OpsItem is created instead.
- [ ] Config compliance dashboard returns to COMPLIANT after remediation without manual action.
- [ ] Runbook failures land in the DLQ/alarm (break the assume role and confirm you are told).
- [ ] Kill switch tested: disabling the EventBridge rule stops remediation within one event.
