---
id: computing-software.cloud-infrastructure-engineering.aws.waf-count-mode-and-rule-action-overrides
name: waf-count-mode-and-rule-action-overrides
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, waf, rule-action-override, count-mode, managed-rule-groups, labels]
level: practitioner
status: docs-checked
description: "Roll out AWS WAF rules safely: start managed groups or single rules in Count, read sampled requests and logs, then switch to Block with rule action overrides."
sources: ["https://docs.aws.amazon.com/waf/latest/developerguide/web-acl-rule-group-override-options.html", "https://docs.aws.amazon.com/waf/latest/developerguide/web-acl-testing.html", "https://docs.aws.amazon.com/waf/latest/developerguide/web-acl-testing-activities.html", "https://docs.aws.amazon.com/waf/latest/developerguide/waf-managed-rule-groups-versioning.html", "https://docs.aws.amazon.com/waf/latest/developerguide/logging-fields.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# WAF Count mode and rule action overrides

AWS WAF documentation now calls the web ACL a protection pack in places; the API and CLI still use `WebACL`.

## 1. Two override levels
- **Whole rule group**: `OverrideAction: {"Count":{}}` instead of `{"None":{}}`: every rule in the group counts
  and nothing from the group blocks.
- **Individual rules**: `RuleActionOverrides` (at most 100) inside `ManagedRuleGroupStatement` sets one rule to
  any valid action (Allow, Block, Count, CAPTCHA, Challenge) while the rest keep their actions; matching requests
  are handled exactly as if that were the rule's action.
```json
{"Name":"AWS-CRS","Priority":10,"OverrideAction":{"None":{}},
 "Statement":{"ManagedRuleGroupStatement":{"VendorName":"AWS","Name":"AWSManagedRulesCommonRuleSet",
   "Version":"<PINNED_VERSION>",
   "RuleActionOverrides":[{"Name":"SizeRestrictions_BODY","ActionToUse":{"Count":{}}}]}},
 "VisibilityConfig":{"SampledRequestsEnabled":true,"CloudWatchMetricsEnabled":true,"MetricName":"crs"}}
```
Your own rules: set `Action: {"Count":{}}`. Count is non-terminating: WAF keeps evaluating the remaining rules, and in
rules you define it can insert custom headers and add labels that other rules can match. CAPTCHA and Challenge incur
extra fees (check the pricing page; not checked here) and act like Count when the request has a valid unexpired token.

## 2. Observe
- CloudWatch metrics: a rule tested in Count mode shows as `CountedRequests`; rule group metrics appear under the
  group, and for a group you do not own your override and any labels still show in your own metrics.
- Sampled requests in the console cover the last 3 hours.
- WAF logs: rules with Count are listed in `nonTerminatingMatchingRules`; Allow and Block rules are the
  `terminatingRule`; rule groups appear under `ruleGroupList`; `labels` lists applied labels (the first 100).
- Test in a staging environment first, then run rules in Count against production traffic before enabling them.
  Changes can take seconds to minutes to propagate, so expect temporary inconsistencies.

## 3. Promote
Remove the override (or set the action to Block) once false positives are handled by:
- a scope-down statement on the managed group,
- a label-match rule after the group that blocks only the labels you trust,
- an allow rule for a known path or IP placed before the group.

## Gotchas
- Pin a specific managed rule group version in production: you can choose the default (the provider manages which
  static version) or a static one, but versions eventually expire and stop being selectable; subscribe to the
  provider's SNS notifications.
- Count rules still add labels, which later rules can act on.

## Verify
- [ ] A week of counted matches reviewed with app owners before switching to Block.

## Checked
Date: 2026-10-27. Documentation release: AWS WAF Developer Guide (latest), botocore wafv2 2019-07-29 model.
Confirmed: `OverrideAction` options, `RuleActionOverrides` structure and 100-item maximum, valid override actions,
Count semantics, 3-hour sampled request window, `CountedRequests`, log field names, 100-label logging limit, version
selection and expiry, and propagation delay. Replaced the pinned `Version_1.12` string with a placeholder and
removed the Athena query (column names not confirmed) and the unconfirmed claim that default versions change
matches.
Method: documentation only; no commands were run.
