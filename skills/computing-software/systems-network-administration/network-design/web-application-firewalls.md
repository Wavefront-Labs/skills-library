---
id: computing-software.systems-network-administration.network-design.web-application-firewalls
name: web-application-firewalls
category: computing-software
field: systems-network-administration
product: network-design
tags: [network-design, firewall-design, waf, owasp-crs, reverse-proxy, application-security]
level: practitioner
status: docs-checked
description: "Deploy a web application firewall: placement (cloud, reverse proxy, inline), OWASP CRS tuning, detection-only rollout, and false positive handling."
sources:
  - https://coreruleset.org/docs/
  - https://owasp.org/www-project-modsecurity-core-rule-set/
  - https://docs.aws.amazon.com/waf/latest/developerguide/waf-chapter.html
  - https://learn.microsoft.com/en-us/azure/web-application-firewall/overview
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Web application firewalls

## Placement
| Option | Examples | Notes |
|---|---|---|
| Cloud/CDN edge | AWS WAF on CloudFront or an Application Load Balancer, Azure WAF on Front Door or Application Gateway | managed service; lock the origin so it only accepts traffic from the WAF |
| Reverse proxy | ModSecurity-compatible engine with the OWASP Core Rule Set | full control; you run it |
| NGFW features | URL/threat profiles | not a substitute for a WAF with HTTP-aware rules |

## OWASP Core Rule Set (CRS)
- The CRS is a generic rule set: read its documentation for how scoring, thresholds and
  paranoia levels work before tuning (not confirmed here).

## Rollout
1. Run in a **detection-only** (log, do not block) mode first, for long enough to see
   representative traffic.
2. Review logs: tune with targeted exclusions for a specific parameter, never disable whole
   rule groups globally.
3. Switch to blocking; add rate limiting and bot rules.
4. Custom virtual patches for known app vulnerabilities while code fixes are pending.

## Cautions
- WAF does not fix vulnerable code; it buys time.
- Ensure the WAF sees the real client IP (X-Forwarded-For trust) and the origin rejects bypass.
- Large uploads/JSON bodies: body inspection limits may let payloads past; configure limits.

## Verify
- [ ] Test payloads (e.g. `?id=1' OR '1'='1`) are blocked and logged; normal user journeys pass with no false positives in a week of logs.

## Checked

- Date: 2026-10-28
- Confirmed: AWS WAF protects CloudFront distributions and Application Load Balancers (AWS WAF developer guide); Azure WAF applies to Application Gateway and Front Door (Azure WAF overview).
- Removed: Cloudflare, Coraza, F5 and nginx claims, CRS anomaly-score threshold and paranoia-level details, directive and action names, the 1-2 week duration (the CRS pages are too short to confirm them).

Method: documentation only; no commands were run.
