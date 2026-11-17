---
id: computing-software.cloud-infrastructure-engineering.aws.eventbridge-input-transformers
name: eventbridge-input-transformers
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, eventbridge, input-transformer, input-path, input-paths-map, input-template, target-input, event-reshaping, aws-eventbridge-predefined, sns-target-message, lambda-target-payload, event-driven]
level: practitioner
status: docs-checked
description: "Reshape an EventBridge event before it hits a target with InputPath, InputPathsMap and InputTemplate: JSON vs string templates, predefined variables, quoting pitfalls and testing."
sources: ["https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-transform-target-input.html"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# EventBridge input transformers

**Goal:** targets receive the payload they want — a Slack-ready sentence, a trimmed JSON
object, a Step Functions input with just the IDs — without a Lambda in the middle whose
only job is to reformat.

## 1. Three ways to shape target input
`put-targets` entries accept **one** of:
- `Input` — a constant JSON string; the event is ignored.
- `InputPath` — a JSONPath selecting a sub-tree: `"$.detail"` delivers only `detail`.
- `InputTransformer` — `InputPathsMap` (named JSONPath extracts) + `InputTemplate` (text with
  `<name>` placeholders).
Omit all three to pass the whole event.

```json
{"Rule":"ec2-stopped","Targets":[{"Id":"slack","Arn":"arn:aws:sns:<REGION>:<ACCOUNT_ID>:ops",
  "InputTransformer":{
    "InputPathsMap":{"instance":"$.detail.instance-id","state":"$.detail.state","acct":"$.account","when":"$.time"},
    "InputTemplate":"\"Instance <instance> in <acct> is now <state> (at <when>)\""}}]}
```
```bash
aws events put-targets --rule ec2-stopped --targets file://targets.json
```

## 2. Template rules that bite
- You can define up to 100 variables in `InputPathsMap`; reference them in the template as `<name>`. Predefined
  variables are reserved and need no path.
- A template can pass a string or JSON. For string variables quotes are optional: EventBridge adds quotes to
  string values when the output is JSON. Do **not** add quotes around variables that hold JSON objects or arrays.
  To output a JSON object from a single path variable put it as a value, for example `{"detail": <detail>}`; used
  inside a larger string the object loses its internal quotes.
- EventBridge does not escape the values it extracts from the event when filling the template.
- A variable whose JSON path does not exist in the event is not created and does not appear in the output. There is
  no validation of the JSON path when you create the rule.
- Predefined variables: `<aws.events.rule-arn>`, `<aws.events.rule-name>`, `<aws.events.event.ingestion-time>`
  (ISO 8601), `<aws.events.event>` (the original event as JSON, without `detail`) and `<aws.events.event.json>`
  (the full original event). The last two can only be used as the value of a JSON field, not inline in a string.
- For multi-line text output wrap each line of the template in double quotes.
- Supported JSONPath: dot notation, dashes, underscores, alphanumerics, array indices (`$.resources[0]`),
  wildcards (`*`) and forward slashes; not all JSONPath syntax is supported.

## 3. Target-specific shapes
- Dynamic path parameters on a target must reference the **original** event, not the transformed one.
- CloudWatch Logs and SSM targets do not support `Input` and `InputPath` in their input transformers.
- For per-target input shapes (SNS message, Lambda event, Step Functions input, SQS body, API destination body,
  ECS overrides) see the target documentation: the transformed text becomes the payload sent to the target.

## 4. Testing
Test with the EventBridge Sandbox in the console (it tests a target input transformer), or point a dev rule
with the same transformer at a CloudWatch Logs target and put a sample event with
`aws events put-events --entries file://e.json`. Keep the sample event in the repo next to the rule.

## Gotchas
- Put the CLI `--targets` JSON in a file: the template is a JSON string containing quotes, and the AWS CLI escapes
  backslashes differently from the console (`"instance \"<instance>\""` renders differently).

## Verify
- [ ] `aws events put-events` with the sample produces the expected string in the CloudWatch Logs target.
- [ ] A placeholder whose path is missing from the event is absent from the output (confirms the failure mode is understood).
- [ ] SNS subscribers receive the human-readable message, not raw JSON.

## Checked

Date 2026-10-23. Documentation release: current Amazon EventBridge User Guide ("Amazon EventBridge input transformation").
Confirmed: 100 variables; predefined variables and their reserved status and JSON-field-only restriction for `aws.events.event` and `aws.events.event.json`; quoting behaviour for strings vs objects; unescaped extraction; missing-path behaviour; supported JSONPath syntax; multi-line string rule; CloudWatch Logs/SSM restriction; dynamic path parameters use the original event; the Sandbox for testing.
Corrected: the draft claimed a missing path makes a JSON template invalid and increments `FailedInvocations`; the docs say the variable is simply not created. The draft's JSONPath limits ("no wildcards") were wrong: wildcards and forward slashes are supported. The "Hyphenated keys need brackets? No" aside was removed.
Removed (not in docs): template size limit, key naming rules, per-target shape rules for SNS Subject, Step Functions, SQS, API destinations and ECS, and the 256 KB output limit.
Sources: https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-transform-target-input.html

Method: documentation only; no commands were run.
