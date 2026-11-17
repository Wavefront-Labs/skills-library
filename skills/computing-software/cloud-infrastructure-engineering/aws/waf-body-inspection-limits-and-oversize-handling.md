---
id: computing-software.cloud-infrastructure-engineering.aws.waf-body-inspection-limits-and-oversize-handling
name: waf-body-inspection-limits-and-oversize-handling
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, waf, body-inspection-limit, oversize-handling, request-body, size-constraint]
level: advanced
status: docs-checked
description: "Handle AWS WAF body inspection limits (8 KB on ALB, configurable to 64 KB on CloudFront and API Gateway) with explicit oversize handling and size rules."
sources: ["https://docs.aws.amazon.com/waf/latest/developerguide/web-request-body-inspection.html", "https://docs.aws.amazon.com/waf/latest/developerguide/web-acl-setting-body-inspection-limit.html", "https://docs.aws.amazon.com/waf/latest/developerguide/aws-managed-rule-groups-baseline.html", "https://docs.aws.amazon.com/waf/latest/developerguide/waf-rule-statement-type-size-constraint-match.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# WAF body inspection limits and oversize handling

## 1. Limits
| Resource | Body bytes inspected |
|---|---|
| Application Load Balancer, AWS AppSync | first 8 KB (8,192 bytes), fixed |
| CloudFront, API Gateway, Cognito, App Runner, Verified Access, Bedrock AgentCore Gateway | 16 KB by default; raise to 32, 48 or 64 KB in the web ACL configuration |
- Headers: at most the first 8 KB (8,192 bytes) and the first 200 headers, whichever limit is reached first; the same
  limits apply to cookies. Inspecting a single named header has no such limit.
- Anything beyond the limits is not inspected, but the whole request is still forwarded if WAF allows it.
- Raising the limit is a pricing consideration: you are charged extra only for requests with bodies larger than the
  default 16 KB (check the AWS WAF pricing page; prices were not checked).
- Request body inspection rules are ignored for gRPC traffic; other rules still apply.

```json
"AssociationConfig":{"RequestBody":{"CLOUDFRONT":{"DefaultSizeInspectionLimit":"KB_32"}}}
```
`DefaultSizeInspectionLimit` takes `KB_16`, `KB_32`, `KB_48` or `KB_64`.

## 2. Oversize handling (per statement on Body, JSON body, headers or cookies)
| Value | Meaning |
|---|---|
| `CONTINUE` | inspect the part within the limit and ignore the rest (a payload placed after the limit is not seen); the default outside the console |
| `MATCH` | treat the request as matching the statement; with a Block action it blocks oversize requests (fail closed) |
| `NO_MATCH` | treat it as not matching and move on to the next rule |
```json
{"ByteMatchStatement":{"FieldToMatch":{"Body":{"OversizeHandling":"MATCH"}}, ...}}
```
In the console you must choose one of the three. Limits and oversize handling apply to rules in managed rule groups
too, so check how a group handles oversize components.

## 3. Practical pattern
- APIs that never take large bodies: a `SizeConstraintStatement` on the body (`ComparisonOperator` `GT`, a `Size`, at
  least one text transformation) with `OversizeHandling: MATCH` and action Block, so attackers cannot pad payloads past
  the inspected bytes.
- If you must allow some oversize requests, add explicit allow rules for only those requests and give them priority
  over other rules that inspect the same component; WAF cannot inspect the oversize part of what you allow.
- The Common Rule Set rule `SizeRestrictions_BODY` blocks request bodies over 8 KB (8,192 bytes); override it to Count
  for upload paths only.

## Verify
- [ ] A 20 KB POST with an injection string after the 8 KB mark is blocked on an ALB by the size rule.
- [ ] Legitimate uploads still succeed on their exempted path.

## Checked
Date: 2026-10-27. Documentation release: AWS WAF Developer Guide (latest), botocore wafv2 2019-07-29 model.
Confirmed: per-resource body limits and the 64 KB maximum with 16 KB steps, header and cookie limits, oversize handling
values and defaults, `SizeInspectionLimit` enum, `SizeConstraintStatement` required fields, gRPC exclusion,
`SizeRestrictions_BODY` threshold and action, and the extra-charge-above-16-KB statement. Rewrote the old
"scope-down exclusion" and "S3 presigned URL" upload advice (no page backs it) as the documented explicit-allow-rule
guidance. Prices were not checked.
Method: documentation only; no commands were run.
