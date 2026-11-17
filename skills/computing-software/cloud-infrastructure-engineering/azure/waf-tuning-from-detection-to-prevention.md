---
id: computing-software.cloud-infrastructure-engineering.azure.waf-tuning-from-detection-to-prevention
name: waf-tuning-from-detection-to-prevention
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, waf, waf-tuning, false-positives, waf-exclusions, application-gateway, front-door]
level: advanced
status: docs-checked
description: "Run the WAF tuning loop on Application Gateway or Front Door: start in Detection, mine WAF logs for false positives, add exclusions or overrides, then switch to Prevention."
sources: ["https://learn.microsoft.com/azure/web-application-firewall/ag/best-practices", "https://learn.microsoft.com/azure/web-application-firewall/afds/waf-front-door-tuning", "https://learn.microsoft.com/azure/web-application-firewall/ag/application-gateway-waf-request-size-limits", "https://learn.microsoft.com/azure/web-application-firewall/ag/application-gateway-waf-configuration"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# WAF tuning: Detection to Prevention

**Goal:** turn on blocking without breaking legitimate traffic.

## Loop
1. **Deploy in Detection mode** with the current managed rule set and diagnostic settings sending WAF logs to Log Analytics. Detection logs what the WAF would do but blocks nothing, so it gives no protection while you tune.
2. **Drive real traffic** long enough to cover releases, admin flows, uploads and API clients.
3. **Mine the logs** in Log Analytics: group matched rules by rule ID and request URI, and rank by hit count. Review the logs regularly; they show both false positives and real attacks.
4. **Classify each hit**: real attack (keep), false positive on a specific field (exclusion), rule irrelevant to the stack (disable or set action to Log for that rule).
5. **Fix narrowly**, in this order of preference:
   - Per-rule exclusion on a named request attribute. Application Gateway per-rule exclusions need OWASP (CRS) 3.2 or later (or Bot Manager 1.0+). Attributes come as keys, names and values (`RequestHeaderValues`, `RequestCookieValues`, `RequestArgValues`, `RequestHeaderKeys`, ...); Microsoft recommends the "values" forms over the older "names" forms. Use `Equals`, not `EqualsAny` (which matches every field).
   - Rule override to Log/disabled for a single rule ID.
   - Per-site/per-URI policy for an app that needs different settings.
6. **Switch to Prevention** once tuned. On Front Door, rule ID 949110 in the logs means the request was blocked by anomaly scoring: tune the rules that contributed to the score.
7. Keep watching: alert on blocked-request spikes after each release.

Define exclusions as code (CLI, PowerShell, Bicep or Terraform) so they can be reapplied when you upgrade the ruleset version; portal-only exclusions must be redone per version.

```bash
az network application-gateway waf-policy managed-rule exclusion rule-set add -g rg --policy-name wafp \
  --type OWASP --version 3.2 --group-name REQUEST-942-APPLICATION-ATTACK-SQLI --rule-ids 942270 \
  --match-variable RequestHeaderValues --match-operator Equals --selector User-Agent
az network application-gateway waf-policy policy-setting update -g rg --policy-name wafp --mode Prevention
```

## Gotchas
- Requests over the body-size or file-upload limits are handled by the size settings, not rule hits: tune the request body size (KB) and file upload limit (MB) settings, or disable body inspection only if justified. In Prevention mode oversized requests are logged and blocked; in Detection mode the body is inspected up to the limit.
- Exclusions can apply to specific rules, a rule set or globally; global exclusions skip every rule for that field, so avoid them.
- Regular expressions are not allowed as exclusion selectors, and XML request bodies are not supported by exclusions.

## Verify
- [ ] No unexplained `Blocked` entries for known-good synthetic tests after switching.
- [ ] Every exclusion has a comment/ticket reference in IaC.

## Checked
Date: 2026-10-31. Confirmed against the Application Gateway WAF best-practices, exclusion-list (waf-configuration), request-size-limits and Front Door WAF tuning pages: Detection logs without blocking; tune then Prevention; exclusions as code; exclusion attribute types and operators; per-rule exclusions need CRS 3.2+; narrow exclusions preferred; the CLI example (taken from the exclusion page); body-size behaviour per mode; rule 949110 as anomaly scoring on Front Door.
Removed as unconfirmed: DRS 2.1 and "blocks at score 5", the 1-2 week traffic window, the sample KQL queries and table/field names, `RequestBodyPostArgNames`/`RequestBodyJsonArgNames`, the 413 claim, and the Front Door Standard managed-rules statement.
Method: documentation only; no commands were run.
