---
id: computing-software.cloud-infrastructure-engineering.aws.lambda-kafka-event-source-mappings
name: lambda-kafka-event-source-mappings
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, lambda, kafka-esm, msk-trigger, self-managed-kafka, event-source-mapping, provisioned-mode, msk]
level: practitioner
status: docs-checked
description: "Consume Kafka with Lambda: MSK and self-managed mappings, IAM/SCRAM/mTLS auth, networking, consumer groups, provisioned pollers, offsets and failure destinations."
sources: ["https://docs.aws.amazon.com/lambda/latest/dg/with-msk.html", "https://docs.aws.amazon.com/lambda/latest/dg/with-msk-permissions.html", "https://docs.aws.amazon.com/lambda/latest/dg/with-msk-configure.html", "https://docs.aws.amazon.com/lambda/latest/dg/kafka-esm-create.html", "https://docs.aws.amazon.com/lambda/latest/dg/invocation-eventsourcemapping.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Lambda Kafka event source mappings (MSK and self-managed)

## 1. MSK mapping
```bash
aws lambda create-event-source-mapping --function-name orders-consumer:live \
  --event-source-arn arn:aws:kafka:<REGION>:<ACCOUNT_ID>:cluster/prod/abcd-1234 \
  --topics orders --starting-position LATEST --batch-size 500 \
  --maximum-batching-window-in-seconds 1 \
  --amazon-managed-kafka-event-source-config '{"ConsumerGroupId":"orders-lambda"}' \
  --provisioned-poller-config '{"MinimumPollers":2,"MaximumPollers":20}'
```
- Execution role: the `AWSLambdaMSKExecutionRole` managed policy holds the minimum: CloudWatch Logs actions,
  `kafka:DescribeClusterV2` (or `kafka:DescribeCluster`), `kafka:GetBootstrapBrokers` and the EC2
  network-interface actions. For IAM auth also grant `kafka-cluster:Connect`, `kafka-cluster:AlterGroup`,
  `kafka-cluster:DescribeGroup`, `kafka-cluster:DescribeTopic` and `kafka-cluster:ReadData`. SASL/SCRAM and mTLS
  use a Secrets Manager secret (`kafka:ListScramSecrets`, `secretsmanager:GetSecretValue`, `kms:Decrypt` if the
  secret uses a customer managed key).
- On-failure destinations need `sqs:SendMessage`, `sns:Publish`, `s3:PutObject` plus `s3:ListBucket`, or
  `kafka-cluster:WriteData` for a Kafka topic.
- Networking: default (on-demand) pollers need a path from the cluster VPC to Lambda, STS and Secrets Manager
  through PrivateLink endpoints or NAT; provisioned mode does not need the endpoints.

## 2. Self-managed Kafka
```bash
aws lambda create-event-source-mapping --function-name f --topics orders --starting-position TRIM_HORIZON \
  --self-managed-event-source '{"Endpoints":{"KAFKA_BOOTSTRAP_SERVERS":["b1.example.com:9092","b2.example.com:9092"]}}' \
  --source-access-configurations '[{"Type":"SASL_SCRAM_512_AUTH","URI":"arn:aws:secretsmanager:<REGION>:<ACCOUNT_ID>:secret:kafka-creds"},{"Type":"VPC_SUBNET","URI":"subnet:subnet-0011001100"},{"Type":"VPC_SECURITY_GROUP","URI":"security_group:sg-0123456789"}]'
```
The VPC entries are needed when only clients inside your VPC can reach the brokers. Other documented
authentication types: `BASIC_AUTH` (SASL/PLAIN), `CLIENT_CERTIFICATE_TLS_AUTH` (mTLS), `OAUTHBEARER_AUTH`,
`IAM_AUTH`, `IAM_OAUTHBEARER_AUTH`. Lambda supports Kafka 0.10.1.0 and later.

## 3. Scaling and ordering
- **Provisioned mode** (min/max pollers) for low-latency or bursty topics: each Kafka poller handles up to 5 MB/s
  or 5 concurrent invokes; minimum 1-200 (default 1), maximum 1-2,000 (default 200). It is billed on poller usage.
- Without provisioned mode Lambda scales pollers automatically based on backlog.
- Lambda reads each partition sequentially; one payload can hold messages from several partitions. Records
  arrive base64 encoded. Default batch size is 100 (max 10,000), default batching window 500 ms.

## 4. Errors and offsets
- If the function errors, Lambda retries the whole batch until it succeeds or the messages expire; set retry
  limits and an **on-failure destination** (SQS, SNS, S3, or a Kafka topic) so a bad record does not stall a partition.
- After each batch Lambda commits the offsets to your Kafka cluster; the starting position decides where a new
  mapping begins.
- Functions behind Kafka mappings support at most a 14 minute timeout.

## Gotchas
- A mapping that stays in a problem state is usually security group, subnet routing or authentication; check
  `StateTransitionReason`.
- The 6 MB invocation payload caps effective batch size for large messages.

## Verify
- [ ] `aws lambda get-event-source-mapping --uuid ...` shows `State: Enabled`.
- [ ] Consumer group lag stays low at peak.
- [ ] A forced failure lands in the on-failure destination and the partition continues.

## Checked
Date 2026-10-23. Lambda Developer Guide MSK, MSK permissions, MSK configure, self-managed Kafka create and event source mapping pages. Confirmed:
MSK role actions and the managed policy, optional IAM-auth `kafka-cluster:*` actions, destination permissions,
endpoint requirement (not in provisioned mode), self-managed CLI shape including `KAFKA_BOOTSTRAP_SERVERS`,
`VPC_SUBNET`/`VPC_SECURITY_GROUP` URI formats, auth type names, poller capacities and ranges, batching defaults, offset
commit after each batch, 14-minute timeout cap. Wrong in the old text: listed `kafka-cluster:DescribeClusterDynamicConfiguration`
(not in the documented set), and described pollers as connecting from the cluster's subnets. Removed
unconfirmed claims: "one concurrent invocation per partition" ceiling, consumer-group rename semantics, MSK lag metric names.
Method: documentation only; no commands were run.
