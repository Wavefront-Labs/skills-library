---
id: computing-software.cloud-infrastructure-engineering.aws.cloudtrail-to-cloudwatch-logs-with-cis-metric-alarms
name: cloudtrail-to-cloudwatch-logs-with-cis-metric-alarms
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, cloudtrail, cloudtrail-cloudwatch, cis-benchmark-alarms, metric-filter, security-monitoring, cloudwatch-logs]
level: practitioner
status: docs-checked
description: "Send a trail to CloudWatch Logs and build the CIS metric-filter alarms (root use, unauthorized calls, IAM/SG/NACL/trail changes, console sign-in without MFA)."
sources: ["https://docs.aws.amazon.com/awscloudtrail/latest/userguide/send-cloudtrail-events-to-cloudwatch-logs.html", "https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudwatch-alarms-for-cloudtrail.html", "https://docs.aws.amazon.com/securityhub/latest/userguide/cloudwatch-controls.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CloudTrail to CloudWatch Logs, with CIS alarms

## 1. Deliver the trail to a log group
```bash
aws logs create-log-group --log-group-name /org/cloudtrail
aws logs put-retention-policy --log-group-name /org/cloudtrail --retention-in-days 90
# role trusted by cloudtrail.amazonaws.com with logs:CreateLogStream and logs:PutLogEvents on the group
aws cloudtrail update-trail --name org-trail \
  --cloud-watch-logs-log-group-arn arn:aws:logs:<REGION>:<ACCOUNT_ID>:log-group:/org/cloudtrail:* \
  --cloud-watch-logs-role-arn arn:aws:iam::<ACCOUNT_ID>:role/CloudTrailToCWL
```
The role needs `logs:CreateLogStream` and `logs:PutLogEvents` on the log group. CloudWatch Logs
ingestion is a separate charge from the S3 copy (see the vendor pricing page).

## 2. The CIS filter set
Create each as a metric filter in namespace `CISBenchmark` with value 1, then an alarm
`Sum >= 1` over 5 minutes to an SNS topic.
| Control | Filter pattern |
|---|---|
| Unauthorized API calls | `{($.errorCode="*UnauthorizedOperation") \|\| ($.errorCode="AccessDenied*")}` |
| Console sign-in without MFA | `{($.eventName="ConsoleLogin") && ($.additionalEventData.MFAUsed != "Yes") && ($.userIdentity.type="IAMUser") && ($.responseElements.ConsoleLogin="Success")}` |
| Root account usage | `{$.userIdentity.type="Root" && $.userIdentity.invokedBy NOT EXISTS && $.eventType !="AwsServiceEvent"}` |
| IAM policy changes | `{($.eventSource=iam.amazonaws.com) && (($.eventName=DeleteGroupPolicy)\|\|($.eventName=DeleteRolePolicy)\|\|($.eventName=DeleteUserPolicy)\|\|($.eventName=PutGroupPolicy)\|\|($.eventName=PutRolePolicy)\|\|($.eventName=PutUserPolicy)\|\|($.eventName=CreatePolicy)\|\|($.eventName=DeletePolicy)\|\|($.eventName=CreatePolicyVersion)\|\|($.eventName=DeletePolicyVersion)\|\|($.eventName=AttachRolePolicy)\|\|($.eventName=DetachRolePolicy)\|\|($.eventName=AttachUserPolicy)\|\|($.eventName=DetachUserPolicy)\|\|($.eventName=AttachGroupPolicy)\|\|($.eventName=DetachGroupPolicy))}` |
| CloudTrail config changes | `{($.eventName=CreateTrail)\|\|($.eventName=UpdateTrail)\|\|($.eventName=DeleteTrail)\|\|($.eventName=StartLogging)\|\|($.eventName=StopLogging)}` |
| Console auth failures | `{($.eventName=ConsoleLogin) && ($.errorMessage="Failed authentication")}` |
| CMK disable/schedule deletion | `{($.eventSource=kms.amazonaws.com) && (($.eventName=DisableKey)\|\|($.eventName=ScheduleKeyDeletion))}` |
| S3 bucket policy changes | `{($.eventSource=s3.amazonaws.com) && (($.eventName=PutBucketAcl)\|\|($.eventName=PutBucketPolicy)\|\|($.eventName=PutBucketCors)\|\|($.eventName=PutBucketLifecycle)\|\|($.eventName=PutBucketReplication)\|\|($.eventName=DeleteBucketPolicy)\|\|($.eventName=DeleteBucketCors)\|\|($.eventName=DeleteBucketLifecycle)\|\|($.eventName=DeleteBucketReplication))}` |
| Config changes | `{($.eventSource=config.amazonaws.com) && (($.eventName=StopConfigurationRecorder)\|\|($.eventName=DeleteDeliveryChannel)\|\|($.eventName=PutDeliveryChannel)\|\|($.eventName=PutConfigurationRecorder))}` |
| Security group changes | `{($.eventName=AuthorizeSecurityGroupIngress)\|\|($.eventName=AuthorizeSecurityGroupEgress)\|\|($.eventName=RevokeSecurityGroupIngress)\|\|($.eventName=RevokeSecurityGroupEgress)\|\|($.eventName=CreateSecurityGroup)\|\|($.eventName=DeleteSecurityGroup)}` |
| NACL changes | `{($.eventName=CreateNetworkAcl)\|\|($.eventName=CreateNetworkAclEntry)\|\|($.eventName=DeleteNetworkAcl)\|\|($.eventName=DeleteNetworkAclEntry)\|\|($.eventName=ReplaceNetworkAclEntry)\|\|($.eventName=ReplaceNetworkAclAssociation)}` |
(In the table `\|\|` is a literal `||` escaped for Markdown. Route table, gateway and VPC change filters follow the same pattern; take the exact event lists from the CloudTrail "CloudWatch alarms for CloudTrail" page.)

Example:
```bash
aws logs put-metric-filter --log-group-name /org/cloudtrail --filter-name RootUsage \
  --filter-pattern '{$.userIdentity.type="Root" && $.userIdentity.invokedBy NOT EXISTS && $.eventType !="AwsServiceEvent"}' \
  --metric-transformations metricName=RootUsage,metricNamespace=CISBenchmark,metricValue=1
aws cloudwatch put-metric-alarm --alarm-name cis-root-usage --namespace CISBenchmark \
  --metric-name RootUsage --statistic Sum --period 300 --evaluation-periods 1 \
  --threshold 1 --comparison-operator GreaterThanOrEqualToThreshold \
  --treat-missing-data notBreaching --alarm-actions arn:aws:sns:<REGION>:<ACCOUNT_ID>:security-alerts
```

## 3. Security Hub checks
Security Hub controls `CloudWatch.1` to `CloudWatch.14` check for these log metric filters and
alarms. In organization member accounts Security Hub generates findings only for member-owned
resources and some controls report `NO_DATA`; decide and document whether central alarms cover
members or each account gets its own filters.

## Verify
- [ ] `aws cloudtrail get-trail-status` shows recent CloudWatch Logs delivery.
- [ ] `aws logs describe-metric-filters --log-group-name /org/cloudtrail` lists all CIS filters.
- [ ] Creating and deleting a test security group in a sandbox fires the SG-change alarm.

## Checked

2026-10-28. Confirmed against AWS documentation: metric filter patterns for unauthorized calls, no-MFA sign-in, root usage, IAM/CloudTrail/KMS/S3/Config/SG/NACL changes and failed console auth; 5-minute Sum period; logs role permissions; CloudWatch.1 to CloudWatch.14 controls and member-account NO_DATA behaviour.
Removed: org-trail single-log-group claim, EventBridge/IA cost advice, route/gateway/VPC and Organizations rows, Security Hub same-account claim, delivery-lag and KMS gotchas, LatestCloudWatchLogsDeliveryTime check; made account ids placeholders.
Method: documentation only; no commands were run.
