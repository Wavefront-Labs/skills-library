---
id: computing-software.cloud-infrastructure-engineering.aws.opensearch-ingestion-pipelines
name: opensearch-ingestion-pipelines
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, opensearch, opensearch-ingestion, osis, data-prepper, ingestion-pipeline, ocu, otel-traces, s3-sqs-source, log-ingestion, fine-grained-access-control, sigv4, dlq]
level: advanced
status: docs-checked
description: "Ingest logs, traces and S3 data into OpenSearch with managed OpenSearch Ingestion (Data Prepper) pipelines: YAML config, roles and FGAC mapping, OCU scaling, DLQs and buffering."
sources: ["https://docs.aws.amazon.com/opensearch-service/latest/developerguide/ingestion.html", "https://docs.aws.amazon.com/opensearch-service/latest/developerguide/creating-pipeline.html", "https://docs.aws.amazon.com/opensearch-service/latest/developerguide/pipeline-domain-access.html", "https://docs.aws.amazon.com/opensearch-service/latest/developerguide/osis-features-overview.html", "https://docs.opensearch.org/latest/data-prepper/", "https://github.com/opensearch-project/documentation-website/tree/main/_data-prepper", "https://github.com/boto/botocore/tree/develop/botocore/data/osis"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OpenSearch Ingestion pipelines

**Goal:** logs, OpenTelemetry traces/metrics, or files landing in S3 flow into an OpenSearch
domain or Serverless collection through a managed, autoscaling Data Prepper pipeline —
parsed and enriched.

## 1. Pipeline configuration (Data Prepper YAML)
S3 objects announced via SQS → parse → OpenSearch:
```yaml
version: "2"
s3-log-pipeline:
  source:
    s3:
      notification_type: sqs
      sqs: { queue_url: "https://sqs.us-east-1.amazonaws.com/<ACCOUNT_ID>/alb-logs-events" }
      compression: gzip
      codec: { newline: {} }
      aws: { region: us-east-1, sts_role_arn: "arn:aws:iam::<ACCOUNT_ID>:role/osis-pipeline" }
  processor:
    # add grok / date processors here for your log format, see the Data Prepper processor docs
    - delete_entries: { with_keys: [message] }
  sink:
    - opensearch:
        hosts: ["https://search-logs-xxxx.us-east-1.es.amazonaws.com"]
        index: "alb-logs"
        aws: { region: us-east-1, sts_role_arn: "arn:aws:iam::<ACCOUNT_ID>:role/osis-pipeline" }
```
Other sources include `http`, `otel_trace_source`, `otel_metrics_source`, `otel_logs_source` and
`kafka`. OpenSearch Ingestion places constraints on the plugins and options you can use: check the
"Supported plugins and options" page.

## 2. Create
```bash
aws osis validate-pipeline --pipeline-configuration-body file://pipeline.yaml
aws osis create-pipeline --pipeline-name alb-logs --min-units 1 --max-units 4 \
  --pipeline-configuration-body file://pipeline.yaml \
  --log-publishing-options IsLoggingEnabled=true,CloudWatchLogDestination={LogGroup=/aws/vendedlogs/OpenSearchIngestion/alb-logs} \
  --buffer-options PersistentBufferEnabled=true \
  --pipeline-role-arn arn:aws:iam::<ACCOUNT_ID>:role/osis-pipeline \
  --vpc-options SubnetIds=subnet-a,subnet-b,SecurityGroupIds=sg-osis
```
- Capacity in **Ingestion OCUs**; capacity scales up and down with usage between the minimum and
  maximum you set (the API requires both, each at least 1). You pay for the OCUs allocated, whether or not
  data flows. Persistent buffering (disk-based, across Availability Zones) is for push-based sources such
  as HTTP and OpenTelemetry.
- VPC options for private domains and push sources reachable only in-VPC.

## 3. Access: the part that fails most
1. The pipeline role trusts `osis-pipelines.amazonaws.com` and has `es:DescribeDomain`,
   `es:ESHttp*` on the domain (for Serverless collections see the collection data access
   policy docs), plus SQS/S3 read.
2. Domain access policy allows the pipeline role.
3. With **fine-grained access control**, map the pipeline role to the OpenSearch `all_access`
   backend role (this adds it as an additional master user), or follow the page's scenarios for an
   internal-database master user. Do this in addition to the domain access policy.
4. Push clients need permission to ingest to the pipeline; see the pipeline security docs.

## Gotchas
- Configure a dead-letter queue on the OpenSearch sink so rejected documents are kept: see the sink docs.
- Index templates/ISM policies are not created by the pipeline; create them first or
  dynamic mapping guesses types.
- `min-units` OCUs are allocated, and billed, whether or not data flows.

## Verify
- [ ] `get-pipeline` status `ACTIVE`; documents appear in the index.
- [ ] A deliberately malformed record lands in the DLQ (if configured).
- [ ] Index has the expected mapping (`GET alb-logs/_mapping`).

## Checked
2026-10-31. Confirmed in the OpenSearch Service pipeline domain-access, ingestion and features-overview pages, the Data Prepper docs (s3 source, date, delete_entries, opensearch sink) and the botocore osis model: `osis-pipelines.amazonaws.com` trust principal, `es:DescribeDomain` and `es:ESHttp*` permissions, FGAC mapping to `all_access`, persistent buffering for push sources, billing by allocated OCUs, create-pipeline parameters (MinUnits and MaxUnits at least 1, BufferOptions, VpcOptions, LogPublishingOptions, PipelineRoleArn). Removed as unconfirmed: OCU vCPU/memory size, the ELB grok pattern and timestamp format, the DLQ block, `osis:Ingest`/SigV4 service name, CloudWatch metric names, blue/green update behaviour and the DynamoDB zero-ETL claim.
Method: documentation only; no commands were run.
