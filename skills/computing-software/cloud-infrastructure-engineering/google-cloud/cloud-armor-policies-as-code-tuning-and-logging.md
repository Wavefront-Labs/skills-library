---
id: computing-software.cloud-infrastructure-engineering.google-cloud.cloud-armor-policies-as-code-tuning-and-logging
name: cloud-armor-policies-as-code-tuning-and-logging
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, cloud-armor, cloud-armor-gcloud, cloud-armor-terraform, named-ip-lists, false-positive-tuning, sensitivity-levels, cloud-armor-logging, armor-monitoring, waf]
level: advanced
status: docs-checked
description: "Manage Cloud Armor with gcloud and Terraform: WAF rule sensitivity, preview mode, opt-outs and field exclusions for false positives, named IP lists, logging."
sources: ["https://cloud.google.com/armor/docs/configure-security-policies", "https://cloud.google.com/armor/docs/waf-rules", "https://cloud.google.com/armor/docs/rule-tuning", "https://cloud.google.com/armor/docs/armor-named-ip", "https://cloud.google.com/armor/docs/request-logging", "https://raw.githubusercontent.com/hashicorp/terraform-provider-google/main/website/docs/r/compute_security_policy.html.markdown"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cloud Armor: policies as code, tuning and logging

## 1. Build a policy with gcloud
```bash
gcloud compute security-policies create edge-waf --type=CLOUD_ARMOR
gcloud compute security-policies rules create 1000 --security-policy=edge-waf \
  --expression="evaluatePreconfiguredWaf('sqli-v33-stable', {'sensitivity': 2})" --action=deny-403 --preview
gcloud compute security-policies rules create 1010 --security-policy=edge-waf \
  --expression="evaluatePreconfiguredWaf('xss-v33-stable', {'sensitivity': 2})" --action=deny-403 --preview
gcloud compute security-policies rules create 900 --security-policy=edge-waf \
  --expression="evaluatePreconfiguredWaf('sourceiplist-fastly')" --action=allow      # named IP list: only CDN egress
gcloud compute security-policies rules create 2000 --security-policy=edge-waf --src-ip-ranges='*' \
  --action=throttle --rate-limit-threshold-count=300 --rate-limit-threshold-interval-sec=60 \
  --conform-action=allow --exceed-action=deny-429 --enforce-on-key=IP
gcloud compute backend-services update web-bes --global --security-policy=edge-waf
```
Lower priority number = evaluated first. Sensitivity ranges 0 to 4 (0 enables no rules; omitted means 4); start low and raise only after tuning.
Named IP lists (`sourceiplist-cloudflare`, `sourceiplist-fastly`, and others on the named IP page) and threat-intel feeds
(`evaluateThreatIntelligence('iplist-tor-exit-nodes')`) avoid hand-maintained CIDRs.

## 2. Terraform
`google_compute_security_policy` with one `rule {}` block per rule (`priority`, `action`, `preview`,
`match { expr { expression = "..." } }`, `rate_limit_options {}`); always keep the default rule
(`priority = 2147483647`) explicit. Review plans — reordering priorities changes behaviour.

## 3. Tune false positives
Enable request logging on the backend (`--enable-logging --logging-sample-rate=1`) and verbose
policy logs (`gcloud compute security-policies update edge-waf --log-level=VERBOSE`) during tuning.
```
resource.type="http_load_balancer"
jsonPayload.previewSecurityPolicy.outcome="DENY"
```
Group by `jsonPayload.previewSecurityPolicy.preconfiguredExprIds` to find noisy signatures, then:
```bash
# opt out a signature
--expression="evaluatePreconfiguredWaf('xss-v33-stable', {'sensitivity': 2, 'opt_out_rule_ids': ['owasp-crs-v030301-id941330-xss']})"
# or exclude a field from inspection
gcloud compute security-policies rules add-preconfig-waf-exclusion 1010 --security-policy=edge-waf \
  --target-rule-set=xss-v33-stable --request-cookie-to-exclude=op=EQUALS,val=session_state
```
Remove `--preview` once preview logs show only true positives.

## 4. Monitor
Alert on spikes in denies and on 429s for rate limits, using the `enforcedSecurityPolicy` log fields. Adaptive Protection raises L7 DDoS alerts with suggested rules (full alerts need Cloud Armor Enterprise).

## Gotchas
- Verbose logging is chatty; turn it back to NORMAL after tuning.
- Behind a third-party CDN, set `userIpRequestHeaders` on the policy so rules see the originating client rather than CDN IPs.

## Verify
- [ ] `curl "https://site/?q=1'%20OR%201=1--"` returns 403 after preview removal.
- [ ] Logs show zero preview DENY hits from known-good test suites.

## Checked
2026-10-28. Confirmed on the Cloud Armor waf-rules, rule-tuning, named IP, request-logging and configure-security-policies pages and the google_compute_security_policy provider doc: `evaluatePreconfiguredWaf` named IP list syntax, `sourceiplist-cloudflare` and `-fastly`, sensitivity range, `opt_out_rule_ids` and rule IDs, `add-preconfig-waf-exclusion` with `--request-cookie-to-exclude`, preview and enforced log fields, `rate_limit_options`, `preview`, `priority` and `match` blocks, default rule priority 2147483647. gcloud commands passed check_commands. Fixed: named IP lists use evaluatePreconfiguredWaf, not evaluatePreconfiguredExpr. Removed: the request_count metric, the Plus tier name, the path-scoping and CDN notes not found in the pages.
Method: documentation only; no commands were run.
