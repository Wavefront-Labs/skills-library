---
id: computing-software.cloud-infrastructure-engineering.alertmanager.sns-sigv4-config
name: sns-sigv4-config
category: computing-software
field: cloud-infrastructure-engineering
product: alertmanager
tags: [alertmanager, sigv4, aws-credentials, sns-config]
level: advanced
status: docs-checked
description: "The sigv4 block of the Alertmanager SNS receiver: region, access_key and secret_key, profile, role_arn and external_id."
sources: ["https://prometheus.io/docs/alerting/latest/configuration/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# sigv4 for SNS

The `sigv4` block in `sns_configs` configures AWS's Signature Version 4 signing of requests.

```yaml
sns_configs:
- topic_arn: arn:aws:sns:us-east-2:123456789012:My-Topic
  sigv4:
    region: us-east-2
    role_arn: arn:aws:iam::123456789012:role/alertmanager
    external_id: my-external-id
```

Fields:
- `region`: the AWS region. If blank, the region from the default credentials chain is used.
- `access_key` and `secret_key`: AWS API keys. Both must be supplied, or both must be blank. If blank, the environment variables `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` are used.
- `profile`: a named AWS profile used to authenticate.
- `role_arn`: an AWS Role ARN, as an alternative to using API keys.
- `external_id`: the AWS External ID used when assuming a role. It can only be used with `role_arn`.

`secret_key` is a `<secret>`; `access_key` is a plain string.

## Checked

2026-11-03. Confirmed against the Alertmanager Configuration page (prometheus.io/docs/alerting/latest/configuration): sigv4_config fields. Removed: closing filler paragraph.

Method: documentation only; no commands were run.
