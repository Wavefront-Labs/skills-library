---
id: computing-software.cloud-infrastructure-engineering.aws.cloudwatch-logs-field-indexes-and-log-transformation
name: cloudwatch-logs-field-indexes-and-log-transformation
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, cloudwatch-logs, field-indexes, log-transformer, logs-insights, index-policy, ingestion-processing]
level: practitioner
status: docs-checked
description: "Speed up and cheapen Logs Insights queries with field index policies, and normalise logs at ingestion with CloudWatch Logs transformers (parseJSON, grok, processors)."
sources: ["https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CloudWatchLogs-Field-Indexing.html", "https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CloudWatch-Logs-Transformation.html", "https://docs.aws.amazon.com/AmazonCloudWatchLogs/latest/APIReference/API_PutIndexPolicy.html", "https://docs.aws.amazon.com/AmazonCloudWatchLogs/latest/APIReference/API_PutTransformer.html", "https://docs.aws.amazon.com/AmazonCloudWatchLogs/latest/APIReference/API_Processor.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CloudWatch Logs field indexes and log transformation

## Field indexes
Index fields you filter on often (request id, user id, trace id) so Logs Insights skips log
events that cannot match.
```bash
aws logs put-index-policy --log-group-identifier /app/orders \
  --policy-document '{"Fields":["requestId","userId","traceId"]}'
aws logs describe-index-policies --log-group-identifiers /app/orders
aws logs describe-field-indexes --log-group-identifiers /app/orders
```
- Account-level index policies (`put-account-policy`, type `FIELD_INDEX_POLICY`) can select log groups by name prefix; a policy applies only in the account where it is created. Standard-class log groups also get default indexes (for example `@logStream` and `traceId`) that do not count toward the quota.
- Query with `filterIndex` (or a plain `filter field = "value"` on an indexed field) to benefit:
```
fields @timestamp, @message
| filterIndex requestId = "c0ffee-42"
| sort @timestamp desc
```
- Only data ingested after the policy exists is indexed, and each event stays indexed for 30 days from ingestion. Indexes help equality and `IN` filters; fields are case-sensitive and only JSON and service log formats are supported.
- `filterIndex` can scan up to 10,000 log groups chosen with up to five name prefixes. Standard log class only (Infrequent Access has no field indexing); check the quotas page for the number of fields per policy.

## Transformers (ingestion-time processing)
```bash
aws logs put-transformer --log-group-identifier /app/nginx --transformer-config '[
  {"renameKeys":{"entries":[{"key":"clientip","renameTo":"client_ip"}]}},
  {"addKeys":{"entries":[{"key":"service","value":"edge"}]}},
  {"lowerCaseString":{"withKeys":["verb"]}}]'
aws logs test-transformer --transformer-config file://t.json --log-event-messages file://samples.json
```
- The example assumes events that already contain `clientip` and `verb` fields (for example JSON events).
- Processors include `parseJSON`, `grok` (`source` and `match`), `csv`, `parseKeyValue`, `listToMap`, `parseToOCSF`, built-ins for AWS formats
  (`parseCloudfront`, `parseVPC`, `parseWAF`, `parseRoute53`, `parsePostgres`), and mutators
  (`addKeys`, `deleteKeys`, `moveKeys`, `renameKeys`, `copyValue`, `typeConverter`, `dateTimeConverter`, string functions such as `lowerCaseString`, `splitString`, `trimString`).
- Original and transformed events are stored with the same retention; view transformed events with Logs Insights, because `GetLogEvents` and `FilterLogEvents` return the originals. Field indexes, discovered fields, metric filters, subscription filters and Contributor Insights can use the transformed fields.
- Transformation happens at ingestion only and is not reversible; events over 512 KB fail transformation.
- Account-level transformers apply to all or many log groups; a log-group-level transformer overrides them.
- Always run `test-transformer` with real samples first (up to 50 sample messages, up to 20 processors per transformer).
- Processors named `parseCloudfront`, `parseVPC`, `parseWAF`, `parseRoute53` and `parsePostgres` must be first in the transformer.

## Gotchas
- Transformers are Standard log class only.
- Transformation and indexing add no retroactive value; plan before incidents.

## Verify
- [ ] Query using `filterIndex` reports lower "records scanned" than an unindexed run.
- [ ] Transformed events show parsed fields in Logs Insights `fields` discovery.

## Checked
Checked 2026-10-27 against the live CloudWatch Logs docs (current release) and the botocore logs 2014-03-28 model.
- Field indexing page: equality and IN benefit, filterIndex up to 10,000 log groups with up to five prefixes, case sensitivity, JSON and service formats only, default indexes, only new events indexed, 30-day index lifetime, policy applies only in its own account. PutIndexPolicy: policyDocument with a Fields array; botocore: put-index-policy, describe-index-policies and describe-field-indexes parameters. PutAccountPolicy: FIELD_INDEX_POLICY and TRANSFORMER_POLICY with name-prefix selection.
- Transformation page: ingestion-only, not reversible, 512 KB limit, original and transformed events kept, GetLogEvents and FilterLogEvents return originals, account-level versus log-group-level precedence, Standard class only. Processor API reference: processor names and which must be first; botocore: 20 processors per transformer, 50 test messages.
- AddKeyEntry, RenameKeyEntry, LowerCaseString and Grok API pages: field names used in the example.
- Removed the grok pattern example (supported patterns are listed on a separate page that was not read) and the claims about index application delay and failed-parse behaviour.

Method: documentation only; no commands were run.
