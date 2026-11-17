---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.ddos-protection
name: ddos-protection
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, infrastructure-protection, ddos-protection, waf, web-application-firewall, shield-advanced, azure-ddos-protection, cloud-armor, bot-management, edge-protection, owasp-top-10]
level: practitioner
status: draft
description: "Protect internet-facing workloads at the edge: CDN in front, managed WAF rules count-then-block, rate-based rules, bot control, DDoS services, origin lockdown."
sources: ["https://docs.aws.amazon.com/whitepapers/latest/aws-best-practices-ddos-resiliency/aws-best-practices-ddos-resiliency.html", "https://learn.microsoft.com/azure/ddos-protection/ddos-protection-overview", "https://cloud.google.com/armor/docs/cloud-armor-overview", "https://owasp.org/www-project-top-ten/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Edge protection with WAF and DDoS mitigation

## Layers
1. **Absorb**: put public endpoints behind a CDN/global edge (CloudFront, Front Door, Cloud CDN /
   global external LB, Cloudflare). Infrastructure-layer DDoS protection is included at the edge
   (AWS Shield Standard, Azure DDoS infrastructure protection, Google's edge).
2. **Filter (L7)**: managed WAF (AWS WAF, Azure WAF on Front Door/App Gateway, Cloud Armor):
   - Managed rule groups (OWASP core rule set / AWS managed rules, known bad inputs, SQLi, IP reputation).
   - **Rate-based rules** per IP / per header (API key) with sensible limits.
   - Bot management for scraping/credential stuffing on login and checkout.
   - Geo or IP allow/deny where business allows.
3. **Advanced DDoS** for critical apps: AWS Shield Advanced (DDoS response team, cost protection),
   Azure DDoS Network Protection, Cloud Armor Enterprise/adaptive protection.
4. **Origin lockdown**: origins accept traffic only from the edge (CloudFront managed prefix list
   / origin-facing security groups, Front Door `X-Azure-FDID` header + service tag, Cloud Armor on
   backends) — otherwise attackers bypass the edge.
5. Scale and cache to survive what gets through; autoscaling max bounds to cap cost.

## Rollout
New WAF rules in **count/detection mode** first, review logs for false positives, then block.
Log WAF to a SIEM; dashboard blocked vs allowed.

## Verify
- [ ] Direct-to-origin requests fail.
- [ ] WAF rules in block mode with known false-positive exceptions documented.
- [ ] DDoS runbook with provider escalation contacts.
