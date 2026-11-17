---
id: computing-software.cybersecurity-defensive.falco.cloud-and-okta-plugins
name: cloud-and-okta-plugins
category: computing-software
field: cybersecurity-defensive
product: falco
tags: [cloudtrail, okta, aws-cloudtrail, sqs, plugin-rules]
level: intro
status: docs-checked
description: "Read AWS CloudTrail logs from S3, SQS or a local path and Okta logs with Falco plugins, with bundled rules and the Okta sample."
sources:
  - https://falco.org/docs/concepts/event-sources/plugins/cloudtrail/
  - https://falco.org/docs/concepts/event-sources/plugins/okta/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The `cloudtrail` plugin reads AWS CloudTrail logs and emits an event per entry. Bundled rules flag console logins without multi-factor authentication, MFA being disabled for users, and encryption being disabled on S3 buckets.

CloudTrail logging must be enabled first for the accounts you monitor. The plugin reads from:
- an S3 bucket;
- an SQS queue receiving SNS notifications about new log files;
- a local filesystem path.

SQS is the easiest to consume, because the plugin sees new files and consumes them automatically, but it needs several AWS resources (queues, topics, subscriptions, IAM policies). The falcosecurity `falco-aws-terraform` module creates them. Configure init and open params under `plugins` in `falco.yaml`.

The `okta` plugin reads Okta logs and emits an event per log entry. Config is the organization API token in init params; it takes no open params. Bundled rules cover creating a user, a locked-out user and admin permissions assigned to a user. A test rule:

```yaml
- rule: Dummy
  desc: Dummy
  condition: okta.app!=""
  output: "evt=%okta.evt.type user=%okta.actor.name ip=%okta.client.ip app=%okta.app"
  priority: DEBUG
  source: okta
```

It alerts for each log entry, for example `evt=user.authentication.sso`.

Note: the sample rule sets `source: okta` to match the plugin's event source.

## Checked

2026-11-08. Read in full: the Falco CloudTrail Events and Okta Events pages (raw markdown under `docs/content/en/docs/concepts/event-sources/plugins/` in falco-website). Confirmed the three CloudTrail read methods, the bundled rules, the Terraform module, the Okta init param and the dummy rule. Removed the unsourced claim that a rule without a matching `source` will not see plugin events.

Method: documentation only; no commands were run.
