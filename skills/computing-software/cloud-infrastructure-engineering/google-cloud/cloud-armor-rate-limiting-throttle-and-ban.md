---
id: computing-software.cloud-infrastructure-engineering.google-cloud.cloud-armor-rate-limiting-throttle-and-ban
name: cloud-armor-rate-limiting-throttle-and-ban
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, cloud-armor, rate-based-ban, throttle-rules, rate-limiting, enforce-on-key, brute-force-protection]
level: practitioner
status: docs-checked
description: "Configure Cloud Armor rate limiting: throttle and rate_based_ban rules, enforce-on-key options (IP, header, cookie, XFF), thresholds, ban duration, preview mode and logging."
sources: ["https://cloud.google.com/armor/docs/rate-limiting-overview", "https://cloud.google.com/armor/docs/configure-rate-limiting", "https://cloud.google.com/sdk/gcloud/reference/compute/security-policies/rules/create", "https://cloud.google.com/armor/docs/rules-language-reference", "https://cloud.google.com/armor/docs/request-logging"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cloud Armor rate limiting: throttle and ban

## Throttle
Allow up to N requests per interval per key; excess gets `exceed-action` (deny-429 etc.).
```bash
gcloud compute security-policies rules create 1000 --security-policy=web-pol \
  --expression="request.path.matches('/api/')" \
  --action=throttle --rate-limit-threshold-count=600 --rate-limit-threshold-interval-sec=60 \
  --conform-action=allow --exceed-action=deny-429 --enforce-on-key=IP
```

## Rate-based ban
If a key exceeds the ban threshold, block it for `ban-duration-sec`:
```bash
gcloud compute security-policies rules create 900 --security-policy=web-pol \
  --expression="request.path == '/login' && request.method == 'POST'" \
  --action=rate-based-ban --rate-limit-threshold-count=20 --rate-limit-threshold-interval-sec=60 \
  --ban-threshold-count=50 --ban-threshold-interval-sec=300 --ban-duration-sec=1800 \
  --conform-action=allow --exceed-action=deny-403 --enforce-on-key=IP
```

## Keys
`--enforce-on-key`: `ALL` (global), `IP`, `HTTP-HEADER` (with `--enforce-on-key-name=X-API-Key`),
`XFF-IP` (first IP in X-Forwarded-For, behind another proxy/CDN), `HTTP-COOKIE`, `HTTP-PATH`,
`SNI`, `REGION-CODE`, `TLS-JA3-FINGERPRINT`, `USER-IP` (also JA4 fingerprint and ASN keys exist). HTTP header, cookie and path
key values are truncated to the first 128 bytes. Combine up to three keys with `--enforce-on-key-configs`
(comma-separated KEY=NAME pairs, e.g. `"HTTP-PATH,HTTP-COOKIE=site_id"`; it replaces `--enforce-on-key` and
`--enforce-on-key-name`). Use several HTTP-HEADER or HTTP-COOKIE keys, but only one of each other key type.

## Limits
- Interval (`--rate-limit-threshold-interval-sec`, `--ban-threshold-interval-sec`): 10, 30, 60, 120, 180, 240, 300, 600, 900, 1200, 1800, 2700 or 3600 seconds.
- `--ban-duration-sec`: 60, 120, 180, 240, 300, 600, 900, 1200, 1800, 2700 or 3600 seconds, counted after the interval ends.
- Count: throttle 1 to 1,000,000; rate-based ban 1 to 10,000.
- `deny` status codes: 403, 404, 429 or 502; Google recommends 429.

## Rollout
1. `--preview` on the rule: logs `previewSecurityPolicy` outcomes without enforcing.
2. Query logs for keys that would be throttled:
   ```
   resource.type="http_load_balancer" jsonPayload.previewSecurityPolicy.outcome="DENY"
   jsonPayload.previewSecurityPolicy.priority=1000
   ```
3. Tune thresholds, remove `--preview`.

## Gotchas
- Thresholds are enforced independently in each region where the backends run, and are approximate: use rate limiting for abuse mitigation, not strict quotas or licensing.
- Clients behind NAT share an IP: prefer header/cookie keys for authenticated APIs.
- Only the highest-priority matching rule applies; lower-priority rules are not evaluated, so a broader allow rule must not outrank the rate limit rule.

## Verify
- [ ] Load test from one IP gets 429 after the threshold; normal users unaffected in logs.

## Checked
Date: 2026-10-28. Confirmed against the Cloud Armor rate limiting overview, Configure rate limiting and Rules language reference pages: key types, three-key limit, 128-byte truncation, interval and ban-duration value lists, count ranges, deny codes, approximate regional enforcement, rule priority behaviour; gcloud flags checked against the CLI reference. Removed: the per-"front-end region" wording and the unsourced priority-number remark. The CEL expressions are examples. The preview log field `previewSecurityPolicy` is on the Cloud Armor request logging page.
Method: documentation only; no commands were run.
