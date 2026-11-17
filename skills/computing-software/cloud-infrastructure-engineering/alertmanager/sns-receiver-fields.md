---
id: computing-software.cloud-infrastructure-engineering.alertmanager.sns-receiver-fields
name: sns-receiver-fields
category: computing-software
field: cloud-infrastructure-engineering
product: alertmanager
tags: [alertmanager, sns-config, topic-arn, aws]
level: advanced
status: docs-checked
description: "sns_configs fields: topic_arn, phone_number, target_arn, subject, message, attributes, api_url and FIFO topic dedup warning."
sources: ["https://prometheus.io/docs/alerting/latest/configuration/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# sns_configs

Alertmanager can publish to Amazon SNS.

```yaml
receivers:
- name: sns
  sns_configs:
  - topic_arn: arn:aws:sns:us-east-2:123456789012:My-Topic
    sigv4:
      region: us-east-2
    attributes:
      severity: '{{ .CommonLabels.severity }}'
```

Fields:
- `send_resolved`: default `true`.
- `api_url`: for example `https://sns.us-east-2.amazonaws.com`; if unspecified the SNS SDK's URL is used.
- `sigv4`: AWS Signature Version 4 signing settings.
- Destination, one of `topic_arn`, `phone_number` (SMS, E.164 format) or `target_arn` (mobile platform endpoint). If you do not specify one, you must specify one of the others.
- `subject`: subject line for email endpoints; default `sns.default.subject`.
- `message`: default `sns.default.message`.
- `attributes`: SNS message attributes, string to string.
- `http_config`: default `global.http_config`.

FIFO topics: set a message group interval longer than 5 minutes so messages with the same group key are not deduplicated by SNS's default deduplication window.

`use_aws_http_client` (default `false`) forces the AWS SDK's own HTTP client, needed for a custom CA bundle and auto-enabled when `AWS_CA_BUNDLE` is set. It disables tracing for SNS, and only `tls_config` and proxy fields of `http_config` are honored.

## Checked

2026-11-03. Confirmed against the Alertmanager Configuration page (prometheus.io/docs/alerting/latest/configuration): sns_config fields, FIFO note, use_aws_http_client.

Method: documentation only; no commands were run.
