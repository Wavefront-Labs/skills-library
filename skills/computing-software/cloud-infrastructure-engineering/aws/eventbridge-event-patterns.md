---
id: computing-software.cloud-infrastructure-engineering.aws.eventbridge-event-patterns
name: eventbridge-event-patterns
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, eventbridge, event-pattern, content-filtering, anything-but, prefix-matching, suffix-matching, numeric-matching, wildcard, exists, equals-ignore-case, or-matching, test-event-pattern, event-rule, rule-matching, event-driven]
level: practitioner
status: docs-checked
description: "Write EventBridge rule event patterns that match exactly what you mean: prefix/suffix, numeric ranges, anything-but, wildcard, exists, $or, nested arrays, and test them with test-event-pattern."
sources: ["https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-create-pattern-operators.html", "https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-event-patterns.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# EventBridge event patterns

**Goal:** rules that fire for exactly the events you intend — not "all EC2 state changes"
when you meant "stopped in production" — written once and proven with `test-event-pattern`
instead of by waiting for production traffic.

## 1. Rules of the language
- A pattern is a JSON object; every **field in the pattern must match** (AND); each field's
  value is an **array of alternatives** (OR). Fields not in the pattern are ignored.
- Matching is exact and case-sensitive unless you use a matcher object such as `equals-ignore-case`.
- Comparison operators work only on **leaf nodes**, except `$or` and `anything-but`.
- If a key appears twice in a pattern only the last reference is used.
- Top-level fields: `source`, `detail-type`, `detail`, `account`, `region`, `resources`,
  `time`, `id`, `version`. `detail` is where service payloads live.

## 2. Matchers
```json
{"source":["aws.ec2"],"detail-type":["EC2 Instance State-change Notification"],
 "detail":{
   "state":["stopped","terminated"],
   "instance-id":[{"prefix":"i-0"}],
   "tags":{"env":[{"equals-ignore-case":"prod"}]}},
 "region":[{"anything-but":["us-east-1"]}]}
```
| Matcher | Syntax | Notes |
|---|---|---|
| prefix / suffix | `[{"prefix":"abc"}]`, `[{"suffix":".png"}]` | `{"prefix":{"equals-ignore-case":"ABC"}}` also allowed |
| anything-but | `[{"anything-but":["a","b"]}]`, `[{"anything-but":{"prefix":"tmp-"}}]`, `[{"anything-but":{"suffix":".txt"}}]`, `[{"anything-but":{"wildcard":"*/lib/*"}}]`, `[{"anything-but":{"equals-ignore-case":"x"}}]` | strings and numbers; prefix, suffix and wildcard take a single value or a list |
| numeric | `[{"numeric":[">",0,"<=",100]}]`, `[{"numeric":["=",100]}]` | 64-bit double comparison; integers exact only within +/-2^53 |
| exists | `[{"exists":true}]` / `false` | leaf nodes only, not intermediate nodes |
| wildcard | `[{"wildcard":"dir/*.png"}]` | any number of `*`, but no consecutive `*`; `\*` and `\\` escape; event bus rules only, not pipes |
| cidr | `[{"cidr":"10.0.0.0/24"}]` | IPv4 and IPv6 |
| null / empty | `[null]`, `[""]` | matches JSON null / empty string |
| `$or` | `{"$or":[{"detail":{"a":["1"]}},{"detail":{"b":["2"]}}]}` | OR across fields |
Complexity limits: a wildcard pattern that is too complex is rejected with `InvalidEventPatternException`
(use fewer wildcards and fewer repeated sequences after a wildcard), and the APIs that accept patterns
(`PutRule`, `CreateArchive`, `UpdateArchive`, `TestEventPattern`) reject patterns where `$or` arrays produce
more than 1,000 rule combinations (multiply the argument counts of each `$or` array).

## 3. Common mistakes
- Pattern values are arrays of alternatives: write `"state":["stopped"]`, not `"state":"stopped"`.
- `exists` does not work on intermediate nodes: `"detail":{"error":[{"exists":false}]}` is only meaningful when `error` is a leaf value.
- Forgetting `source` on a custom bus means every `detail-type` from every producer matches.
- Values are case-sensitive: `"detail-type":["EC2 Instance State-change Notification"]` matches that exact
  string; use `{"equals-ignore-case":"ec2 instance state-change notification"}` if casing varies.

## 4. Test before you deploy
```bash
aws events test-event-pattern --event-pattern file://pattern.json --event file://sample.json   # → {"Result": true}
```
`TestEventPattern` is the API behind this check. Use a realistic sample event with the standard top-level fields
(`version`, `id`, `detail-type`, `source`, `account`, `time`, `region`, `resources`, `detail`), taken from the
service's documented sample events.

## 5. Patterns for custom events
Publish with a stable contract: `source: "com.example.orders"`, `detail-type: "OrderPlaced"`,
`detail` with a `version` field. Consumers match on `detail-type` and `detail.version`
prefix; producers can then add fields without breaking rules. Keep `detail-type` as a
human-readable event name, not a type code.

## Gotchas
- A pattern that uses more than 1,000 `$or` combinations, or an over-complex wildcard pattern, is rejected when you create the rule.

## Verify
- [ ] `test-event-pattern` returns true for a sample matching event and false for one with `state: running`.
- [ ] The rule's `MatchedEvents`/`Invocations` metrics increase after a real event; `TriggeredRules` on the bus equals expected count.
- [ ] A deliberately mis-cased `detail-type` in the pattern returns false in the test (confirms case sensitivity understood).

## Checked

Date 2026-10-23. Documentation release: current Amazon EventBridge User Guide, "Comparison operators for use in event patterns".
Confirmed: top-level event fields; operators and syntax (prefix, suffix, anything-but variants, numeric incl. `=`, exists on leaf nodes only, wildcard rules and complexity, cidr IPv4/IPv6, null, empty string, equals-ignore-case, `$or`); duplicate-key behaviour; numeric precision limit; 1,000-combination limit for `$or`; APIs that validate patterns include `TestEventPattern`.
Corrected: the garbled combination-limit sentence ("5 wildcard chars... no") now states the documented limits; the wildcard rule is "any number of `*`, no consecutive wildcards".
Removed (not in docs pages read): event-array matching rule wording, `InvalidEventPatternException` for string-valued fields, numeric-vs-string remark, `time`/`id` remark, S3 detail-type example, catch-all rule trick, console sandbox note, CloudTrail read-only-event remark, pattern-plus-schedule invalidity.
Sources: https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-create-pattern-operators.html ; https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-event-patterns.html

Method: documentation only; no commands were run.
