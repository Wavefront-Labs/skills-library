---
id: computing-software.cybersecurity-defensive.cloud-security.aws-waf-configuration
name: aws-waf-configuration
category: computing-software
field: cybersecurity-defensive
product: cloud-security
tags: [cloud-network-security, aws-waf, web-application-firewall, managed-rule-groups, rate-based-rules, bot-control, waf-logging, count-mode]
level: practitioner
status: docs-checked
description: "Configure AWS WAF on CloudFront/ALB/API Gateway: managed rule groups, rate-based rules, count-mode tuning, scope-down statements, logging and body limits."
sources: ["https://docs.aws.amazon.com/waf/latest/developerguide/aws-managed-rule-groups-baseline.html", "https://docs.aws.amazon.com/waf/latest/developerguide/aws-managed-rule-groups-ip-rep.html", "https://docs.aws.amazon.com/waf/latest/developerguide/waf-rule-action.html", "https://docs.aws.amazon.com/waf/latest/developerguide/waf-rule-statement-type-rate-based-request-limiting.html", "https://docs.aws.amazon.com/waf/latest/developerguide/logging-cw-logs.html", "https://docs.aws.amazon.com/waf/latest/developerguide/logging-management-configure.html", "https://docs.aws.amazon.com/waf/latest/developerguide/aws-waf-capacity-units.html", "https://docs.aws.amazon.com/waf/latest/developerguide/waf-oversize-request-components.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AWS WAF configuration

**Goal:** filter common web attacks and abusive traffic in front of applications with low
false positives and full visibility. AWS docs now call a web ACL a "protection pack (web ACL)".

## Web ACL baseline (in priority order)
1. Allow-list rule for health checks/known partners (narrow; by header or IP set).
2. **AWSManagedRulesAmazonIpReputationList** and **AWSManagedRulesAnonymousIpList** (IP reputation rule groups; block or count).
3. **Rate-based rule** per IP, plus tighter rules scoped to sensitive paths such as a login page using a **scope-down statement** (only requests matching it are aggregated, counted and limited).
4. **AWSManagedRulesCommonRuleSet** (core rule set), **AWSManagedRulesKnownBadInputsRuleSet**, and any other managed groups that match your stack.
5. Optional: Bot Control, Account Takeover Prevention (ATP) for login, Account Creation Fraud Prevention (ACFP) for sign-up. Check AWS WAF Pricing for the extra fees on these and on CAPTCHA/Challenge actions.
6. Default action: Allow.

## Deploy in count mode first
The **Count** action counts a request without allowing or blocking it and is non-terminating: processing continues with the remaining rules, and you can add labels that later rules match. Run managed groups in Count (override the rule actions), analyse logs, then switch to Block group by group. For a rule causing false positives (for example `SizeRestrictions_BODY`, which flags bodies over 8 KB, on upload endpoints) use a rule action override on that rule rather than disabling the whole group.

## Logging
Choose a logging destination (CloudWatch Logs, S3 or Firehose) whose name begins with `aws-waf-logs-`; a CloudWatch log group may have any suffix after that prefix. Redact sensitive fields in the logging configuration; redacted fields appear as `xxx`.

## Capacity
The base price of a protection pack (web ACL) includes 1,500 WCUs; using more incurs additional fees. The maximum capacity is 5,000 WCUs for a web ACL and for a rule group.

## Gotchas
- A WAF on an ALB does not see traffic that reaches the origins directly: restrict origins.
- Body inspection is limited: ALB and AppSync inspect the first 8 KB; CloudFront, API Gateway, Cognito, App Runner and Verified Access inspect 16 KB by default, configurable up to 64 KB. Headers and cookies are limited to the first 8 KB or 200 items. Choose the oversize handling deliberately.

## Verify
- [ ] Test requests with SQLi/XSS payloads are blocked; legitimate test suite passes.
- [ ] Logs reach the SIEM; blocked request dashboard reviewed weekly.

## Checked
Checked 2026-11-09 against the AWS WAF Developer Guide pages in `sources` (managed rule group names, Count action, rate-based scope-down, logging name prefix and redaction, WCU figures, oversize body/header limits). Removed unconfirmed claims: the example rate figure and window, the CloudWatch Logs Insights query, Firewall Manager and Terraform resource mentions, managed rule version pinning, and the 1-2 week count-mode duration.
Method: documentation only; no commands were run.
