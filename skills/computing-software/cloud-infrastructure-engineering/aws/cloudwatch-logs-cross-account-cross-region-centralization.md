---
id: computing-software.cloud-infrastructure-engineering.aws.cloudwatch-logs-cross-account-cross-region-centralization
name: cloudwatch-logs-cross-account-cross-region-centralization
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, cloudwatch-logs, log-centralization, cross-account-observability, subscription-filters, log-destinations, oam]
level: practitioner
status: docs-checked
description: "Centralise CloudWatch Logs across accounts and regions: org centralization rules, cross-account observability links, and subscription filter destinations to Firehose or S3."
sources: ["https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CloudWatchLogs_Centralization.html", "https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CrossAccountSubscriptions.html", "https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/SubscriptionFilters.html", "https://docs.aws.amazon.com/OAM/latest/APIReference/API_CreateLink.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cross-account, cross-region log centralization

## Three patterns
| Pattern | Data copied? | Best for |
|---|---|---|
| Cross-account observability (OAM sink and links) | no, query in place | engineers searching logs/metrics/traces of many accounts from one console |
| Log centralization rules (Organizations) | yes, into a central account/region | central retention, security, single bill for storage |
| Subscription filters to a cross-account destination | yes, streamed | SIEM/OpenSearch/S3 data lake, real-time processing |

## Cross-account observability
```bash
# monitoring account
aws oam create-sink --name org-sink
aws oam put-sink-policy --sink-identifier "$SINK" --policy file://allow-org.json
# each source account
aws oam create-link --label-template '$AccountName' \
  --resource-types AWS::Logs::LogGroup AWS::CloudWatch::Metric AWS::XRay::Trace \
  --sink-identifier "$SINK"
```
Logs Insights in the monitoring account can query source log groups.

## Centralization rules
CloudWatch Logs centralization works with AWS Organizations: rules replicate log data from source accounts and Regions into a destination account and Region, optionally with a backup Region and tag propagation. Only log data that arrives after the rule exists is centralized. An organization can have 50 organization centralization rules by default (adjustable, quota read 2026-10-27). Check the pricing page for the cost of the copy.

## Subscription filter to a destination
```bash
# central account: destination fronting a Firehose stream
aws logs put-destination --destination-name central-logs \
  --target-arn arn:aws:firehose:eu-west-1:999999999999:deliverystream/central \
  --role-arn arn:aws:iam::999999999999:role/CWLtoFirehose
aws logs put-destination-policy --destination-name central-logs --access-policy file://org-policy.json
# source account
aws logs put-subscription-filter --log-group-name /app/orders --filter-name to-central \
  --filter-pattern "" --destination-arn arn:aws:logs:eu-west-1:999999999999:destination:central-logs
```
- The log group and the destination must be in the same Region (the resource the destination points to can be elsewhere). The destination access policy names the source accounts allowed to subscribe.
- Up to 5 subscription filters per log group and one account-level subscription filter per Region (quota read 2026-10-27); account-level filters apply to all log groups in the account.
- Payloads are base64 encoded and gzip compressed. Centralized log groups expose `@aws.account`, `@aws.region` and `@source.log` for use in subscription filters.

## Gotchas
- A destination must be in the log group's Region, so use one destination per Region or centralization rules for cross-Region collection; data transfer between Regions has a cost.
- Centralization rules have encryption settings for copied log groups that were encrypted with customer managed KMS keys; configure them when creating the rule.

## Verify
- [ ] A test event from a member account appears centrally (query or S3 object) within minutes.
- [ ] New accounts get links or filters through your account-provisioning automation or org-level rules.

## Checked
Checked 2026-10-27 against the live CloudWatch docs and the OAM API reference (current release), and the botocore oam 2022-06-10 and logs 2014-03-28 models.
- Log centralization page: Organizations-based rules, destination account and Region, backup Region, tag propagation, only new data. CloudWatch quotas page: 50 organization centralization rules.
- Cross-account subscriptions pages: destination wraps a stream, Firehose and Kinesis walkthroughs, same-Region rule for log group and destination, @aws.account, @aws.region, @source.log. Subscription filter quotas: 5 per log group, one account-level filter per Region.
- OAM API reference and botocore: create-sink --name, put-sink-policy --sink-identifier --policy, create-link --label-template, --resource-types, --sink-identifier; AWS::Logs::LogGroup, AWS::CloudWatch::Metric and AWS::XRay::Trace resource types and the $AccountName label template.
- Removed unconfirmed claims: the first-copy pricing remark, aws:PrincipalOrgID in destination policies, Firehose decompression, per-Region links, the storage-doubling remark, StackSets deployment.

Method: documentation only; no commands were run.
