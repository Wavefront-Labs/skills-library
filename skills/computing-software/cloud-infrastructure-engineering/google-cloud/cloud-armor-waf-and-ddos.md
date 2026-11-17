---
id: computing-software.cloud-infrastructure-engineering.google-cloud.cloud-armor-waf-and-ddos
name: cloud-armor-waf-and-ddos
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, cloud-armor, waf, ddos, rate-limiting, preconfigured-waf-rules, owasp-crs, sqli, xss, custom-rules-language, cel-armor, geo-blocking, bot-management, recaptcha-enterprise, adaptive-protection, security-policies, edge-security-policy, preview-mode, threat-intelligence, cloud-armor-enterprise]
level: practitioner
status: docs-checked
description: "Protect apps with Cloud Armor: policies in preview mode, OWASP WAF rules tuned by sensitivity, rate limiting and bans, geo and threat-intel rules, reCAPTCHA, Adaptive Protection."
sources: ["https://cloud.google.com/armor/docs/cloud-armor-overview", "https://cloud.google.com/armor/docs/configure-security-policies", "https://cloud.google.com/armor/docs/waf-rules", "https://cloud.google.com/armor/docs/rate-limiting-overview", "https://cloud.google.com/armor/docs/rules-language-reference", "https://cloud.google.com/armor/docs/adaptive-protection-overview", "https://cloud.google.com/armor/docs/bot-management"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Cloud Armor WAF and DDoS

**Goal:** L7 attacks and abusive clients are dropped at Google's edge before they reach
your backends, without the WAF blocking real customers — because every rule went through preview first.

## 1. Policy skeleton
```bash
gcloud compute security-policies create web-policy --type=CLOUD_ARMOR
gcloud compute security-policies update web-policy --json-parsing=STANDARD --log-level=VERBOSE
# default rule (priority 2147483647) is allow; make it explicit
gcloud compute security-policies rules update 2147483647 --security-policy=web-policy --action=allow
# attach
gcloud compute backend-services update web-bs --global --security-policy=web-policy
```
- `--type` chooses a backend security policy or an edge security policy. Edge policies can filter only on `origin.asn`, `origin.ip`, `origin.region_code`, `request.headers`, `request.method`, `request.path`, `request.query` and `request.scheme`.
- Lower priority number = evaluated first; first match wins. Keep allow-lists (monitoring probes, partners) at low numbers, WAF in the middle, rate limits after, default deny/allow last.

## 2. Preconfigured WAF rules (OWASP CRS)
```bash
gcloud compute security-policies rules create 1000 --security-policy=web-policy \
  --expression="evaluatePreconfiguredWaf('sqli-v33-stable', {'sensitivity': 2})" --action=deny-403 --preview
gcloud compute security-policies rules create 1010 --security-policy=web-policy \
  --expression="evaluatePreconfiguredWaf('xss-v33-stable', {'sensitivity': 2, 'opt_out_rule_ids': ['owasp-crs-v030301-id941340-xss']})" --action=deny-403 --preview
```
Sets include `sqli`, `xss`, `scannerdetection`, `protocolattack`, `sessionfixation`, `nodejs` and `cve-canary`; the waf-rules page lists every set and the current version (newer sets are `-v422-stable`, older ones `-v33-stable`). **Sensitivity** runs 0 to 4: 0 enables no rules, and if omitted all signatures run (level 4). Lower levels give fewer false positives; start low and raise per set after reviewing preview logs.
Workflow: `--preview` → run on real traffic → query `jsonPayload.previewSecurityPolicy` in LB logs → `opt_out_rule_ids` the signatures that hit legitimate traffic → remove `--preview`.

## 3. Custom rules (CEL)
```
# geo + path
origin.region_code in ['RU','KP'] && request.path.startsWith('/admin')
# threat intel feeds
evaluateThreatIntelligence('iplist-tor-exit-nodes') || evaluateThreatIntelligence('iplist-known-malicious-ips')
# plain CIDRs
inIpRange(origin.ip, '203.0.113.0/24')
# header/UA
has(request.headers['user-agent']) && request.headers['user-agent'].matches('(?i)sqlmap|nikto')
```
Attributes: `origin.ip`, `origin.region_code`, `origin.asn`, `request.method`, `request.path`, `request.query`, `request.headers`, `token.recaptcha_action.score`.

## 4. Rate limiting and bans
```bash
gcloud compute security-policies rules create 2000 --security-policy=web-policy \
  --expression="request.path.startsWith('/api/login')" --action=rate-based-ban \
  --rate-limit-threshold-count=20 --rate-limit-threshold-interval-sec=60 \
  --ban-threshold-count=100 --ban-threshold-interval-sec=600 --ban-duration-sec=1800 \
  --conform-action=allow --exceed-action=deny-429 --enforce-on-key=IP      # or HTTP-HEADER, HTTP-COOKIE, XFF-IP, HTTP-PATH, SNI, REGION-CODE
```
`throttle` (per-key limit, no ban) vs `rate-based-ban`. `--enforce-on-key-configs` combines keys (IP + path). `exceed-action=redirect --exceed-redirect-type=GOOGLE_RECAPTCHA` challenges instead of blocking.

## 5. Bots and Adaptive Protection
- **reCAPTCHA Enterprise** integration: `token.recaptcha_action.score` (0.0 to 1.0) rules for action tokens, or a `redirect` action of type `GOOGLE_RECAPTCHA` (`--action=redirect --redirect-type=GOOGLE_RECAPTCHA`); a user who passes the assessment gets an exemption cookie.
- **Adaptive Protection** raises alerts with a suggested rule: copy its CEL expression into the match condition of a new rule. Full alerts need Cloud Armor Enterprise; otherwise you get only a basic alert.

## Gotchas
- If a third-party CDN fronts the load balancer, configure `userIpRequestHeaders` on the policy (and consider `--enforce-on-key=XFF-IP`) so rules see the originating client.
- Logs use separate fields: `previewSecurityPolicy` for preview rules and `enforcedSecurityPolicy` for enforced ones; alerts should read the latter.
- Preconfigured WAF rules evaluate only the first 64 kB of the request body.

## Verify
- [ ] `curl "https://host/?q=1' OR 1=1--"` returns 403 and the LB log shows `enforcedSecurityPolicy.outcome: DENY` with the matched `preconfiguredExprIds`.
- [ ] 25 rapid login POSTs from one IP → 429, then banned for 30 min; a different IP unaffected.
- [ ] Preview-mode rule hits are reviewed weekly; false-positive signature IDs are in `opt_out_rule_ids`, not the whole set disabled.
- [ ] Adaptive Protection alert received in a load test (logged under the Network Security Policy resource in Cloud Logging).

## Checked
2026-10-28. Confirmed on the Cloud Armor waf-rules, rules-language-reference, rate-limiting, configure-rate-limiting, bot-management, adaptive-protection, request-logging and configure-security-policies pages: sensitivity range and default, rule-set names, `opt_out_rule_ids`, 64 kB body limit, enforce-on-key values, `deny-429`, rate-based-ban options, GOOGLE_RECAPTCHA redirect and exemption cookie, `token.recaptcha_action.score`, `userIpRequestHeaders`, edge-policy attribute list, log fields. gcloud commands and flags passed check_commands. Fixed: body limit was 8 KB, edge policies are not IP/geo only, TLS-JA3 key and sensitivity range. Removed: Managed Protection Plus rename, DDoS bill protection, response team, auto-deploy flags, rule sets not found (lfi, rfi, rce, php, java, methodenforcement), regional-policy and JSON-parsing remarks.
Method: documentation only; no commands were run.
