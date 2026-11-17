---
id: computing-software.cloud-infrastructure-engineering.aws.lambda-amazon-mq-and-documentdb-event-sources
name: lambda-amazon-mq-and-documentdb-event-sources
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, lambda, mq-trigger, documentdb-change-streams, event-source-mapping, amazon-mq]
level: advanced
status: docs-checked
description: "Trigger Lambda from Amazon MQ (ActiveMQ/RabbitMQ) queues and DocumentDB change streams with event source mappings: auth secrets, VPC networking and retention."
sources: ["https://docs.aws.amazon.com/lambda/latest/dg/with-mq.html", "https://docs.aws.amazon.com/lambda/latest/dg/process-mq-messages-with-lambda.html", "https://docs.aws.amazon.com/lambda/latest/dg/with-documentdb.html", "https://docs.aws.amazon.com/documentdb/latest/developerguide/change_streams.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Amazon MQ and DocumentDB change stream event sources

## 1. Amazon MQ
```bash
aws lambda create-event-source-mapping --function-name mq-consumer \
  --event-source-arn arn:aws:mq:<REGION>:<ACCOUNT_ID>:broker:orders:b-1234 \
  --queues orders.in --batch-size 100 --maximum-batching-window-in-seconds 5 \
  --source-access-configurations '[{"Type":"BASIC_AUTH","URI":"arn:aws:secretsmanager:<REGION>:<ACCOUNT_ID>:secret:mq-user"}]'
```
- RabbitMQ also needs the virtual host in the source access configuration (the console field is "Source access configuration: virtual host information and the Secrets Manager secret").
- Function role: `mq:DescribeBroker`, `secretsmanager:GetSecretValue`, `ec2:CreateNetworkInterface`,
  `ec2:DeleteNetworkInterface`, `ec2:DescribeNetworkInterfaces`, `ec2:DescribeSecurityGroups`,
  `ec2:DescribeSubnets`, `ec2:DescribeVpcs`, plus `logs:CreateLogGroup`, `logs:CreateLogStream`,
  `logs:PutLogEvents`; add `kms:Decrypt` when a customer managed key encrypts the secret.
- Limits per mapping: ActiveMQ runs at most 5 concurrent execution environments, RabbitMQ 1 (raising
  reserved or provisioned concurrency does not change this; ask Support per mapping UUID). Only queue
  destinations, no cross-account brokers, ActiveMQ SimpleAuthenticationPlugin or RabbitMQ PLAIN auth only.
- Private brokers: the mapping needs AWS PrivateLink endpoints for Lambda, STS and Secrets Manager (or a NAT
  gateway); provisioned-mode mappings do not need the endpoints. Default broker ports: 61617 (ActiveMQ),
  5671 (RabbitMQ). Allow the port from the mapping's security group (self-referencing rule works).
- Message bodies arrive base64-encoded (`data`). If the function errors on any message, Lambda retries the
  whole batch until it succeeds or the messages expire. Mappings are at-least-once: make the function idempotent.
- Functions behind MQ and DocumentDB mappings support a maximum timeout of 14 minutes.

## 2. DocumentDB change streams
Enable on the collection first (empty strings act as wildcards for database or collection):
```javascript
db.adminCommand({modifyChangeStreams: 1, database: "shop", collection: "orders", enable: true});
```
```bash
aws lambda create-event-source-mapping --function-name orders-cdc \
  --event-source-arn arn:aws:rds:<REGION>:<ACCOUNT_ID>:cluster:docdb-prod \
  --starting-position LATEST --batch-size 100 \
  --document-db-event-source-config '{"DatabaseName":"shop","CollectionName":"orders","FullDocument":"UpdateLookup"}' \
  --source-access-configurations '[{"Type":"BASIC_AUTH","URI":"arn:aws:secretsmanager:<REGION>:<ACCOUNT_ID>:secret:docdb-cdc"}]'
```
- Supported: DocumentDB 4.0 and 5.0, instance-based or regional clusters, same account and Region as the
  function. Not supported: 3.6, elastic clusters, global clusters. Events are processed sequentially, so one
  concurrent invocation.
- Role needs `rds:DescribeDBClusters`, `rds:DescribeDBClusterParameters`, `rds:DescribeDBSubnetGroups`, the
  same `ec2:` network interface actions as above, `kms:Decrypt` and `secretsmanager:GetSecretValue`.
- Change stream retention is the cluster parameter `change_stream_log_retention_duration`: events are kept 3
  hours by default and the retention can be set between 1 hour and 7 days. If the function falls further behind
  or is disabled longer than that, events are lost. Raise it for safety.
- TLS must stay enabled on the cluster (the default) or Lambda cannot connect. Networking is as for MQ
  (endpoints for Lambda, STS and Secrets Manager, or NAT); default port 27017.
- `FullDocument` is `Default` (a delta only) or `UpdateLookup` (delta plus the entire document).
- Events over 6 MB are dropped and `OversizedRecordCount` is emitted. With `LATEST`, events can be missed
  while the mapping is created or updated; use `TRIM_HORIZON` or `AT_TIMESTAMP` if that matters.
- Event filtering is not supported for DocumentDB.

## Verify
- [ ] `aws lambda get-event-source-mapping --uuid <UUID>` shows `State: Enabled` and `LastProcessingResult: OK`.
- [ ] Inserting a test document or message triggers one invocation.

## Checked
Date 2026-10-23. Lambda Developer Guide and DocumentDB Developer Guide pages in `sources` (current release). Confirmed: MQ concurrency, auth and
destination limits, role actions, ports, endpoint requirement and provisioned-mode exception, retry-whole-batch
behaviour, 14-minute timeout cap; DocumentDB supported versions and cluster types, role actions, 3 hour default
and 1 hour to 7 day retention range, modifyChangeStreams syntax, FullDocument values, 6 MB drop, no filtering.
Removed unconfirmed claims about broker redelivery policy and DLQ.
Method: documentation only; no commands were run.
