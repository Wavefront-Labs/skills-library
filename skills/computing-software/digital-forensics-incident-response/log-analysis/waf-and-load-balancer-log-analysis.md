---
id: computing-software.digital-forensics-incident-response.log-analysis.waf-and-load-balancer-log-analysis
name: waf-and-load-balancer-log-analysis
category: computing-software
field: digital-forensics-incident-response
product: log-analysis
tags: [waf-logs, load-balancer-logs, aws-alb, dfir]
level: practitioner
status: docs-checked
description: "Use AWS ALB access logs and AWS WAF logs to find the client, blocked requests, rule matches and the join key to backend logs."
sources: ["https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-access-logs.html", "https://docs.aws.amazon.com/waf/latest/developerguide/logging-fields.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# WAF and load balancer logs (AWS)

**Goal:** see web attacks at the edge, including blocked ones, and bridge to backend logs.

## ALB access logs
- Optional, disabled by default; delivered to S3 as compressed files, one per load balancer
  node every 5 minutes. Delivery is eventually consistent and can contain multiple logs for
  the same period. Logging is best effort: use it to understand requests, not as a complete
  accounting.
- Requests that never reached a target (malformed, no healthy targets) are still logged.
- Entries are space-delimited. New fields are added at the end, so parse only to the last
  documented field. Fields in order include: type, time, elb, `client:port`, `target:port`,
  request_processing_time, target_processing_time, response_processing_time, elb_status_code,
  target_status_code, received_bytes, sent_bytes, "request_line", "user_agent", ssl_cipher,
  ssl_protocol, target_group_arn, "trace_id", "domain_name", "chosen_cert_arn",
  matched_rule_priority, request_creation_time, "actions_executed", "redirect_url",
  "error_reason", and later fields such as classification and conn_trace_id.
- `client:port` holds the proxy's address if a proxy sits in front of the load balancer.
- `trace_id` is the contents of the X-Amzn-Trace-Id header.
- `actions_executed` values: authenticate, fixed-response, forward, redirect, rewrite, waf.
  If waf is the final action, AWS WAF rejected the request; by default it is logged as 403 in
  `elb_status_code` (or the custom response code), and `target:port` is `-`.
- `target_status_code` is recorded only if a target connection was made and it responded.
- Processing times are -1 when the request could not be dispatched to a target.
- The request line preserves the URL as the client sent it.

## AWS WAF logs (selected fields)
- `action`: terminating action (allow, block, CAPTCHA, challenge). `terminatingRuleId` is the
  rule that ended inspection; `Default_Action` if nothing terminated. `terminatingRuleType`:
  RATE_BASED, REGULAR, GROUP, MANAGED_RULE_GROUP.
- `nonTerminatingMatchingRules`: matched non-terminating rules (count, CAPTCHA, challenge),
  so counted matches still show in the log. `ruleGroupList`: rule groups that acted on the
  request. `excludedRules`: rules excluded (set to Count) in a rule group.
- `labels`: labels applied by rules (first 100 logged).
- `httpRequest`: includes `clientIp`, `country`, `uri`, `args`, `httpMethod`, `headers`,
  `httpVersion`. `httpSourceName` shows the source (CF, ALB, APIGW and others) and
  `httpSourceId` the resource.
- `ja3Fingerprint` and `ja4Fingerprint`: TLS Client Hello hashes, available only for
  CloudFront and ALB.
- `requestId`: for ALB this is the trace ID, so it joins to the ALB `trace_id`.
- `ruleMatchDetails`/`terminatingRuleMatchDetails` are populated only for SQL injection and
  XSS match statements. Further matches may exist, because inspection stops at the first
  terminating rule.
- `rateBasedRuleList`: rate-based rules evaluated, with limitKey, maxRateAllowed and
  evaluationWindowSec.
- `oversizeFields`: inspected fields over the inspection limit.

## Analyses
- Compare blocked and allowed requests from the same client IP: did any variant get through?
- Review non-terminating matches on requests that were allowed.
- Join WAF `requestId` to ALB `trace_id`, then to backend logs.

## Gotchas
- ALB logs are off by default; enable before an incident.
- ALB `time` is when the load balancer generated the response; `request_creation_time` is when
  it received the request (both ISO 8601).
- Azure Front Door, Cloudflare and ModSecurity logging are not covered here (pages not read).

## Checked
2026-11-09. Confirmed on the ALB access logs page (read in full to Actions taken) and the WAF log fields page (read in full). Removed: Azure Front Door, Cloudflare and ModSecurity claims and source, Athena query, X-Forwarded-For/CF-Connecting-IP advice, WAF sampling and body truncation claims, cloudflare tag, x-forwarded-for tag.
Method: documentation only; no commands were run.
