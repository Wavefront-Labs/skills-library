---
id: computing-software.firmware-embedded-development.iot-protocols.aws-iot-rules
name: aws-iot-rules
category: computing-software
field: firmware-embedded-development
product: iot-protocols
tags: [aws-iot-rules, aws-iot-core, aws-iot, rule-sql, topic-rule, action, iot-protocols]
level: practitioner
status: docs-checked
description: "AWS IoT rules engine: Route device data to AWS services."
sources:
  - https://docs.aws.amazon.com/iot/latest/developerguide/iot-rules.html
  - https://docs.aws.amazon.com/iot/latest/developerguide/iot-rule-actions.html
  - https://docs.aws.amazon.com/iot/latest/developerguide/rule-error-handling.html
  - https://docs.aws.amazon.com/iot/latest/developerguide/iot-basic-ingest.html
  - https://docs.aws.amazon.com/iot/latest/developerguide/iot-sql-reference.html
  - https://docs.aws.amazon.com/iot/latest/developerguide/iot-sql-functions.html
  - https://docs.aws.amazon.com/iot/latest/developerguide/iot-substitution-templates.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AWS IoT rules engine

**Goal:** Route device data to AWS services.

## Steps
1. SQL: SELECT temperature, topic(2) AS device FROM 'dev/+/telemetry' WHERE temperature > 30
2. Actions: Lambda, DynamoDB, S3, Kinesis, SNS, Timestream, republish
3. Add an error action to catch failures
4. Basic Ingest publishes directly to $aws/rules/<rule>/... to skip messaging cost; the device policy needs publish permission on $aws/rules/* or $aws/rules/<rule>/*, and nothing can subscribe to those topics
5. AWS IoT needs permission to reach the target resources, so give each action an IAM role with only the access it needs
6. Substitution templates like ${topic(2)} build keys
7. Define the rule in the same AWS Region as the target service resource
8. topic(n) returns the n-th topic segment (1-based): for foo/bar/baz, topic(2) is bar

## Gotcha
After retries fail, the message is discarded and the error only appears in CloudWatch Logs; set an error action and enable AWS IoT CloudWatch logging to see failures.

## Verify
- [ ] Test message hits target service
- [ ] Error action stores failed payload
- [ ] Role least privilege

## Checked
Confirmed 2026-11-08 against AWS IoT Core Developer Guide pages "Rules for AWS IoT", "AWS IoT rule actions" (action list, same-Region note, retry then discard), "Error handling (error action)", "Reducing messaging costs with Basic Ingest", "AWS IoT SQL reference" (SELECT, FROM, WHERE form) and "AWS IoT SQL functions" (topic(n) entry only, partial read) and "Substitution templates" (partial read: the topic() example and the no-alias rule). Role least-privilege is advice that rests on the page statement that rules need granted permission to your AWS resources.
Method: documentation only; no commands were run.
