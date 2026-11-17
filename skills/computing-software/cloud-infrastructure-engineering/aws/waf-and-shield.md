---
id: computing-software.cloud-infrastructure-engineering.aws.waf-and-shield
name: waf-and-shield
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, waf, aws-waf, wafv2, shield, shield-advanced, ddos-protection, web-acl, managed-rule-groups, rate-based-rule, rate-limiting, bot-control, account-takeover-prevention, wcu, count-mode, scope-down-statement, waf-logging, captcha, challenge, firewall-manager, layer-7-protection, srt, cost-protection, web-application-firewall]
level: practitioner
status: draft
description: "Protect CloudFront, ALB and API Gateway with AWS WAF (web ACLs, managed and rate-based rules, count-first rollout, logging) and decide when Shield Advanced pays off."
sources: ["https://docs.aws.amazon.com/waf/latest/developerguide/web-acl-setting-body-inspection-limit.html", "https://docs.aws.amazon.com/waf/latest/developerguide/waf-rule-statement-type-rate-based-high-level-settings.html", "https://docs.aws.amazon.com/waf/latest/developerguide/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AWS WAF and Shield — layer-7 filtering and DDoS posture

**Goal:** every internet-facing HTTP entry point sits behind a web ACL that blocks
known-bad traffic and rate-limits abuse, rolled out in count mode so legitimate users
are never blocked by surprise, with logs that explain every block; and a deliberate
yes/no on Shield Advanced. Entry points are built in `...aws.cloudfront-distributions`
and `...aws.elastic-load-balancing`.

## 1. Web ACL placement and scope
- `--scope CLOUDFRONT` web ACLs must be created in **us-east-1** and attach to
  distributions; `--scope REGIONAL` ones live in the resource's region and attach to
  ALB, API Gateway (REST stages), AppSync, Cognito user pools, App Runner, Verified
  Access. One ACL can protect many resources; one resource takes one ACL.
- Protect at the **outermost** layer: if CloudFront fronts the ALB, put WAF on
  CloudFront and lock the ALB to CloudFront (prefix list / origin secret) so the ALB
  ACL is unnecessary. API Gateway HTTP APIs cannot take WAF — front them with CloudFront.
- Capacity: each rule costs **WCUs**; a web ACL gets 1,500 by default (raisable to
  5,000 at extra cost). Managed groups list their WCU; `AWSManagedRulesCommonRuleSet`
  alone is 700.

## 2. Rule stack that works for most apps
Evaluation is by **priority** (lowest first); the first *terminating* action
(allow/block/captcha/challenge) ends it, `count` and labels do not. Typical order:
1. **Allow** list: your own CIDRs / health checkers / partner IPs via an **IP set**
   (`create-ip-set`), scoped to a path if possible.
2. `AWSManagedRulesAmazonIpReputationList` and `AWSManagedRulesAnonymousIpList`
   (Tor, VPNs, hosting providers — use *count* on the hosting-provider rule or you
   block CI pipelines and legitimate API clients).
3. `AWSManagedRulesCommonRuleSet` (OWASP-style: XSS, LFI, bad user agents, size
   limits) — expect to override `SizeRestrictions_BODY` to count for upload endpoints
   and `NoUserAgent_HEADER` for internal clients.
4. `AWSManagedRulesKnownBadInputsRuleSet` (Log4j JNDI, path traversal probes),
   `AWSManagedRulesSQLiRuleSet` for anything with a database, plus the platform set
   (`AWSManagedRulesLinuxRuleSet`, `WordPressRuleSet`…) matching your stack.
5. **Rate-based rule** per source IP: `--statement 'RateBasedStatement={Limit=1000,
   EvaluationWindowSec=300,AggregateKeyType=IP}'` (minimum limit 10; windows 60, 120,
   300, 600 s). Aggregate by `FORWARDED_IP` (`X-Forwarded-For`) when a proxy sits in
   front, or by custom keys (header, cookie, URI path, label) for login endpoints:
   e.g. `/login` limited to 20 per 5 min per IP with a **scope-down statement** on the path.
6. **Bot Control** (`AWSManagedRulesBotControlRuleSet`, `COMMON` or `TARGETED`
   inspection level — targeted adds ML and browser challenges, costs more), and
   **ATP** (account takeover: credential-stuffing detection on your login path, needs
   the request fields mapped) / **ACFP** (fake account creation) where relevant.
   These are priced per request on top of base WAF; scope them down to the paths
   they protect.
7. Default action **allow**; set **block** only for an allowlisted-IP-only admin ACL.
Custom responses (`custom-response-bodies` + `CustomResponse` on the block action)
return a branded 403/429 and a header you can grep for; **CAPTCHA** and **Challenge**
actions stop simple bots without blocking humans (challenge is invisible, needs the
JS SDK for API clients).

## 3. Roll out in count, read the logs, then block
- Attach every managed group with `--override-action Count={}` first, run for a week,
  then query which rules would have blocked: logging must be on —
  `put-logging-configuration --resource-arn <ACL> --log-destination-configs
  arn:aws:logs:…:log-group:aws-waf-logs-prod` (the CloudWatch log group **name must
  start with `aws-waf-logs-`**; S3 and Firehose also accepted). Redact sensitive
  fields (`RedactedFields`) and add a logging filter to keep only `BLOCK`/`COUNT` if
  volume is a cost problem.
- Logs Insights: `fields httpRequest.clientIp, terminatingRuleId, action |
  filter action = "BLOCK" | stats count() by terminatingRuleId` and look at
  `nonTerminatingMatchingRules` for what count-mode would have done.
- Flip groups to their default action one at a time; keep specific rule overrides as
  **rule action overrides** (`RuleActionOverrides`) rather than editing the group.
- **Labels** let one rule classify and a later rule act: e.g. managed group adds
  `awswaf:managed:aws:bot-control:bot:category:search_engine`; your rate rule excludes
  that label so Googlebot is never throttled.
- Sampled requests (console, 3 hours) are enough for a quick look; CloudWatch metrics
  per rule (`BlockedRequests`, `CountedRequests`) feed alarms on sudden spikes.

## 4. Limits that surprise
- Body inspection: fixed 8 KB for ALB and AppSync; for CloudFront, API Gateway, Cognito and
  similar the default is 16 KB, raisable in 16 KB steps to 64 KB (extra charge above 16 KB). Anything beyond is
  **not inspected** — pick the oversize handling (`CONTINUE`, `MATCH`, `NO_MATCH`)
  per rule consciously; upload endpoints usually want `CONTINUE`.
- JSON body parsing is opt-in per rule (`JsonBody` field-to-match); without it SQLi
  rules see the JSON as a string.
- A web ACL change takes up to a minute to propagate; IP set updates are faster.
- Pricing: per web ACL, per rule (managed groups count as one rule each), per million
  requests, plus the intelligent threat add-ons (Bot Control, ATP, ACFP) per request.
- **Firewall Manager** (from the Organizations delegated admin) pushes a baseline
  web ACL to every in-scope resource in every account and re-attaches it if someone
  removes it; use it once you have more than a handful of accounts.

## 5. Shield: Standard vs Advanced
- **Shield Standard** is always on for every AWS customer: network/transport-layer
  (SYN floods, reflection) mitigation at the edge for CloudFront, Route 53, Global
  Accelerator and, to a degree, ELB/EIP. You cannot configure it; architecture is the
  lever — CloudFront + Route 53 in front of everything internet-facing gives the most
  absorption.
- **Shield Advanced** (subscription with a term commitment plus data-transfer fees; see the
  Shield pricing page): protect specific resources (CloudFront, Route 53 zones,
  Global Accelerator, ALB, NLB, EIPs); gets you the **Shield Response Team** (SRT —
  grant them a role to apply WAF rules during an attack, enable *proactive
  engagement* with a Route 53 health check they watch), **application-layer automatic
  mitigation** (Shield writes rate rules into your web ACL — requires WAF on the
  resource), **health-based detection**, near-real-time attack diagnostics,
  **protection groups** to aggregate many resources, and **cost protection** — credits
  for the scaling charges (CloudFront, Route 53, ELB, EC2) incurred during a confirmed attack.
  It also waives the per-request WAF charges for protected resources, which can make it
  close to cost-neutral for very high-traffic sites. It is worth it when a day of
  downtime costs more than USD 36,000 or when a compliance owner needs a named
  response team; otherwise WAF rate rules + CloudFront + autoscaling are the answer.
- `aws shield describe-attack-statistics` / `list-attacks` show what Shield has seen;
  the **Global threat dashboard** is free.

## Gotchas
- A web ACL attached to CloudFront only sees traffic *through* CloudFront — an ALB left
  publicly reachable bypasses it.
- `AWSManagedRulesCommonRuleSet` version pins: a group attached with the default
  version auto-updates and can start blocking after an AWS change; subscribe to the
  SNS topic for the group or pin a version and review.
- Rate-based rules count *requests*, not failed logins; brute-force needs ATP or an
  app-side counter.
- Blocking by country (`GeoMatchStatement`) uses the client IP (or forwarded IP if you
  configure it) and misses VPN users; use it for compliance, not security.
- WAF cannot inspect TLS it does not terminate: for NLB pass-through there is no WAF.

## Verify
- [ ] Every internet-facing ALB/CloudFront/API has a web ACL (Config rule `alb-waf-enabled`, `cloudfront-associated-with-waf`); none is reachable around it.
- [ ] Logging on with the `aws-waf-logs-` prefix; a Logs Insights query shows blocks by rule for the last 24 h.
- [ ] A curl with `User-Agent: ""` or a `?id=1' OR 1=1--` probe returns the custom 403; normal user journeys (login, upload, checkout) pass with zero counted matches on the blocking rules.
- [ ] Rate rule trips on a scripted burst to `/login` and clears after the window.
- [ ] Shield decision recorded: either Advanced with SRT role, proactive engagement health check and protection groups configured, or Standard with the architectural mitigations listed.
