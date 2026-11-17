---
id: computing-software.cybersecurity-defensive.system-hardening.modsecurity-owasp-crs
name: modsecurity-owasp-crs
category: computing-software
field: cybersecurity-defensive
product: system-hardening
tags: [web-server-hardening, owasp-crs, modsecurity, coraza, paranoia-level, anomaly-scoring, waf-tuning, web-application-firewall]
level: advanced
status: draft
description: "Run ModSecurity or Coraza with the OWASP Core Rule Set: install, paranoia levels, anomaly scoring thresholds, detection-only rollout, rule exclusions for false positives, logging."
sources: ["https://coreruleset.org/docs/", "https://coreruleset.org/docs/concepts/false_positives_tuning/", "https://coraza.io/docs/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# ModSecurity / Coraza with the OWASP Core Rule Set

CRS is a generic attack-detection rule set (SQLi, XSS, RCE, LFI, scanners, protocol violations) for
ModSecurity v3 (libmodsecurity with nginx connector), ModSecurity v2 (Apache), and Coraza (Go; Caddy,
Envoy/proxy-wasm, HAProxy SPOA).

## Install (nginx + libmodsecurity example)
```
load_module modules/ngx_http_modsecurity_module.so;
modsecurity on;
modsecurity_rules_file /etc/nginx/modsec/main.conf;
```
`main.conf`:
```
Include /etc/nginx/modsec/modsecurity.conf      # SecRuleEngine DetectionOnly initially
Include /etc/nginx/modsec/crs/crs-setup.conf
Include /etc/nginx/modsec/crs/rules/*.conf
```

## Key settings (crs-setup.conf)
- **Paranoia level** (`tx.blocking_paranoia_level`): 1 default (few false positives), 2 for sensitive apps,
  3-4 high assurance with heavy tuning.
- **Anomaly scoring**: rules add scores; request blocked when `tx.inbound_anomaly_score_threshold`
  (default 5 = one critical match) is reached. Start with a high threshold (e.g. 100) in blocking mode or
  DetectionOnly, then lower stepwise to 5.
- `tx.detection_paranoia_level` can be higher than blocking to log extra signals without blocking.

## Rollout
1. DetectionOnly for 1-4 weeks with full audit logging (`SecAuditEngine RelevantOnly`, JSON format).
2. Analyse matches by rule ID and URI; separate attacks from false positives.
3. Write exclusions, then enable blocking with a high threshold, lower over time.

## False-positive exclusions (place in REQUEST-900 / RESPONSE-999 exclusion files)
Narrowest form first: exclude one argument from one rule on one path.
```
SecRule REQUEST_URI "@beginsWith /api/cms/save" \
  "id:1000,phase:1,pass,nolog,ctl:ruleRemoveTargetById=942100;ARGS:body"
```
Startup-time: `SecRuleUpdateTargetById 941100 "!ARGS:html_content"`.
Avoid `SecRuleRemoveById` globally. CRS ships application exclusion plugins (WordPress, Nextcloud, Drupal).

## Logging
Audit log fields: matched rule IDs, anomaly scores, unique transaction ID (also send as a response header
for support tickets). Ship to SIEM; alert on blocked requests to sensitive endpoints and on spikes.

## Gotchas
- Request body limits (`SecRequestBodyLimit`) and JSON/XML body processors must be enabled to inspect APIs.
- CRS is generic; it is not a substitute for fixing vulnerabilities or for virtual patches tailored to a CVE.
- Performance: high paranoia levels and response body inspection cost CPU.

## Verify
`curl "https://site/?q=1%27%20OR%20%271%27=%271"` returns 403 in blocking mode with a logged 942xxx rule,
and the regression test suite of the app passes without CRS blocks.
