---
id: computing-software.cloud-infrastructure-engineering.aws.sns-filter-policies
name: sns-filter-policies
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, sns, filter-policy, filter-policy-scope, message-filtering, message-attributes, message-body-filtering, subscription-filter, numeric-matching, prefix-matching, anything-but, exists, fan-out, messaging]
level: practitioner
status: docs-checked
description: "Write SNS subscription filter policies (attribute or body scope) with exact, prefix, numeric, anything-but and exists matchers, and alarm on silently filtered-out messages."
sources: ["https://docs.aws.amazon.com/sns/latest/dg/sns-subscription-filter-policies.html", "https://docs.aws.amazon.com/sns/latest/dg/subscription-filter-policy-constraints.html", "https://docs.aws.amazon.com/sns/latest/dg/string-value-matching.html", "https://docs.aws.amazon.com/sns/latest/dg/sns-monitoring-using-cloudwatch.html", "https://docs.aws.amazon.com/sns/latest/dg/fifo-message-delivery.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SNS subscription filter policies

**Goal:** one topic, many subscribers, each receiving exactly the subset it wants — filtered
at SNS, not in consumer code that discards 90% of what it is paid to receive.

## 1. Attach a policy
```bash
aws sns subscribe --topic-arn "$TOPIC" --protocol sqs --notification-endpoint "$QUEUE_ARN" \
  --attributes '{"FilterPolicyScope":"MessageAttributes","FilterPolicy":"{\"eventType\":[\"order.paid\",\"order.refunded\"],\"region\":[{\"prefix\":\"eu-\"}]}"}'
aws sns set-subscription-attributes --subscription-arn "$SUB" --attribute-name FilterPolicy --attribute-value '{"eventType":["order.paid"]}'
```
Policy semantics: every **key** in the policy must match (AND); within a key the list is OR.
A message missing a key the policy names does **not** match (unless `exists:false`).

## 2. Scope: attributes vs body
- `FilterPolicyScope: MessageAttributes` (default) — matches on message attributes of type `String`,
  `String.Array` and `Number`; attributes of type `Binary` are ignored. Nested policies are not accepted.
  You must double-escape double quotes and backslashes in attribute-based policies or the policy will not match.
- `FilterPolicyScope: MessageBody` — payload-based filtering on the **JSON** body (a body that is not valid
  JSON is counted by `...FilteredOut-InvalidMessageBody`). Nested policies are accepted, for example
  `{"detail":{"state":["RUNNING"]}}`; only leaf keys count toward the key limit.
Publishers must set attributes with the right type:
```bash
aws sns publish --topic-arn "$TOPIC" --message '{"orderId":"1"}' \
  --message-attributes '{"eventType":{"DataType":"String","StringValue":"order.paid"},"amount":{"DataType":"Number","StringValue":"120.5"}}'
```

## 3. Matchers
| Matcher | Example | Note |
|---|---|---|
| exact | `["order.paid"]` | case-sensitive |
| prefix / suffix | `[{"prefix":"order."}]`, `[{"suffix":".paid"}]` | |
| anything-but | `[{"anything-but":["test"]}]`, `[{"anything-but":{"prefix":"debug."}}]` | also suffix and wildcard forms |
| numeric | `[{"numeric":[">=",100,"<",1000]}]` | exact, anything-but and range matching |
| exists | `[{"exists":true}]` / `false` | key matching; `false` = key must be absent |
| equals-ignore-case | `[{"equals-ignore-case":"Paid"}]` | |
| IP | `[{"cidr":"10.0.0.0/24"}]` | string value |
| wildcard | `[{"wildcard":"*ball"}]` | `*` matches any characters |
| `$or` | `{"$or":[{"a":["1"]},{"b":["2"]}]}` | OR across keys |

For `String.Array` attributes each element is treated as a separate string for exact matching; `anything-but`
matches if none of the elements is listed.

## 4. Limits that matter
- A policy can have at most **5 keys** (for nested body policies only leaf keys count).
- The total combination of values must not exceed **150**: multiply the number of values in each array
  (3 keys with 10 values each is 1,000 and is not allowed). Split subscribers or use prefixes.
- Wildcard patterns have a complexity budget: at most 100 points across all fields and 3 wildcards per pattern.
- Maximum policy size is 256 KB, passed as a valid UTF-8 string; defaults are 200 filter policies per topic and
  10,000 per account (raise with Service Quotas).
- Additions or changes to a filter policy take up to 15 minutes to fully take effect.
- String matching is case-sensitive. Numeric values range from -10^9 to 10^9 with five digits after the decimal point.

## 5. Dropped messages are invisible by default
A message rejected by a subscription's filter policy is not delivered to that subscription; the CloudWatch
metrics `NumberOfNotificationsFilteredOut`, `...FilteredOut-MessageAttributes`, `...FilteredOut-MessageBody`,
`...FilteredOut-InvalidAttributes`, `...FilteredOut-NoMessageAttributes` and `...FilteredOut-InvalidMessageBody`
(namespace `AWS/SNS`, dimension `TopicName`) count them. `NumberOfNotificationsFailed` does not include
filtered messages. Alarm on the filtered-out metrics if "a subscriber stopped receiving" would otherwise be
found by the customer.

## Gotchas
- When SNS evaluates a policy it ignores message attributes or body properties that the policy does not name.
- The policy scope is a separate subscription attribute (`FilterPolicyScope`); set the scope that matches
  how the policy is written.
- On FIFO topics filtering is supported, but a filtered subscription gets at-most-once delivery.

## Verify
- [ ] Publish with `eventType=order.paid` → only the paid-subscriber queue gets it; `order.cancelled` → `NumberOfNotificationsFilteredOut` increments by one per non-matching subscription.
- [ ] Publishing **without** attributes to a topic whose subscriptions all filter on attributes yields `NumberOfNotificationsFilteredOut-NoMessageAttributes` > 0.
- [ ] `aws sns get-subscription-attributes` echoes the exact policy JSON and scope.

## Checked

Date 2026-10-23. Documentation release: current Amazon SNS Developer Guide (subscription filter policies, constraints, string value matching, CloudWatch metrics).
Confirmed: scope default `MessageAttributes` and the `MessageBody` option; filterable attribute types and that Binary is ignored; nested policies only for payload filtering; operator list (exact, prefix, suffix, anything-but incl. prefix, equals-ignore-case, cidr, numeric forms, key matching, `$or`, wildcard); limits (5 keys, 150 combinations, 256 KB, 200 per topic, 10,000 per account, 15-minute propagation, numeric range and precision, case-sensitive strings); all FilteredOut metric names; FIFO at-most-once note.
Corrected: the draft's garbled limits paragraph ("5 keys ... no: 5 nesting levels") and the invented error text; the draft's metric `...FilteredOut-InvalidAttributes` list is now complete.
Removed (not in docs): policy non-retroactivity, raw-delivery attribute visibility notes, scope-change ordering, "top-level JSON object" rule.
Sources: https://docs.aws.amazon.com/sns/latest/dg/sns-subscription-filter-policies.html ; https://docs.aws.amazon.com/sns/latest/dg/subscription-filter-policy-constraints.html ; https://docs.aws.amazon.com/sns/latest/dg/string-value-matching.html ; https://docs.aws.amazon.com/sns/latest/dg/sns-monitoring-using-cloudwatch.html ; https://docs.aws.amazon.com/sns/latest/dg/fifo-message-delivery.html

Method: documentation only; no commands were run.
