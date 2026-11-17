---
id: computing-software.cloud-infrastructure-engineering.azure.waf-policies-and-ddos-protection
name: waf-policies-and-ddos-protection
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, waf, web-application-firewall, waf-policy, owasp-crs, drs, default-rule-set, managed-rules, custom-rules, rate-limiting, geo-filtering, bot-protection, bot-manager, detection-mode, prevention-mode, exclusions, anomaly-scoring, false-positives, waf-logs, ddos-protection, ddos-network-protection, ddos-ip-protection, ddos-rapid-response, front-door-waf, application-gateway-waf]
level: advanced
status: draft
description: "Run WAF on Front Door or App Gateway: managed DRS/CRS rules with anomaly scoring, exclusions tuned from logs, rate-limit/geo/bot custom rules, detection-to-prevention; DDoS Network vs IP Protection."
sources: ["Microsoft Learn - Azure Web Application Firewall on Azure Front Door and on Application Gateway", "Microsoft Learn - Tuning Web Application Firewall for Azure Front Door / troubleshooting false positives", "Microsoft Learn - Custom rules and rate limiting for WAF", "Microsoft Learn - Azure DDoS Protection overview (Network Protection vs IP Protection)", "Microsoft Learn - WAF logs and KQL examples"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# WAF and DDoS — managed rules you've tuned, not just turned on

**Goal:** a WAF in Prevention mode that blocks real attacks and not your own JSON
APIs, with the evidence in Log Analytics; and DDoS protection where it changes the outcome.

## 1. Where the WAF lives
- **Front Door WAF** (global, Standard: custom rules; Premium: managed **DRS 2.1** + Bot Manager) — the default for internet apps.
- **Application Gateway WAF_v2** (regional, **OWASP CRS 3.2** / DRS 2.1 on newer policies) for apps without Front Door or needing regional inspection.
- Both chained = double inspection; keep the AGW policy in Detection or minimal rules.
Policy is a separate resource associated to routes/domains (AFD) or to the gateway/listener/path (AGW).
```bash
az network front-door waf-policy create -g rg -n wafprod --sku Premium_AzureFrontDoor --mode Detection --request-body-check Enabled
az network front-door waf-policy managed-rules add -g rg --policy-name wafprod --type Microsoft_DefaultRuleSet --version 2.1 --action Block
az network front-door waf-policy managed-rules add -g rg --policy-name wafprod --type Microsoft_BotManagerRuleSet --version 1.1
az afd security-policy create -g rg --profile-name afd-prod -n sp-web --domains <endpoint-or-custom-domain-ids> --waf-policy <policy-id>
# AGW: az network application-gateway waf-policy create ... ; managed-rule-set add --type OWASP --version 3.2 ; associate with --waf-policy on the gateway
```

## 2. Managed rules and anomaly scoring
- DRS 2.x / CRS 3.2 are **anomaly-scoring**: each matched rule adds a score (Critical 5,
  Error 4, Warning 3, Notice 2); request blocked when total ≥ 5 (paranoia level 1). So one
  critical rule blocks; two warnings don't. `action` on the rule set is the block action; per-rule overrides set `Allow`/`Block`/`Log`/`Redirect` (AFD) or enable/disable with `Log`/`Block` (AGW).
- Rule groups: `SQLI`, `XSS`, `RCE`, `PROTOCOL-ENFORCEMENT`, `PROTOCOL-ATTACK`, `LFI`, `RFI`, `PHP`, `JAVA`, `SESSION-FIXATION`, `MS-ThreatIntel-*`.
- Request body inspection cap (128 KB AGW / AFD policy setting); enforce max body size or large uploads get blocked/bypass inspection — decide.

## 3. Tune from Detection to Prevention
1. Deploy in **Detection**; diagnostic settings → `FrontDoorWebApplicationFirewallLog` / `ApplicationGatewayFirewallLog`.
2. After a week:
```kusto
AzureDiagnostics | where Category == "FrontDoorWebApplicationFirewallLog" and action_s in ("Block","AnomalyScoring")
| summarize hits=count(), uris=make_set(requestUri_s, 5) by ruleName_s, details_matches_s | order by hits desc
```
   (resource-specific table names vary; AGW: `ApplicationGatewayFirewallLog` with `ruleId_s`, `Message`, `details_data_s`.)
3. For each false positive: prefer an **exclusion** scoped to the rule or rule group and the
   exact selector (`RequestHeaderNames`/`RequestCookieNames`/`RequestBodyPostArgNames`/`RequestBodyJsonArgNames` `Equals` `payload`) over disabling the rule: `az network front-door waf-policy managed-rules exclusion add --type Microsoft_DefaultRuleSet --version 2.1 --rule-group-id SQLI --rule-id 942430 --match-variable RequestBodyJsonArgNames --operator Equals --value "query"`.
4. Known noisy rules for JSON/REST APIs: 942430/942440 (SQL chars in free text), 920300/920320
   (missing Accept/User-Agent — bots and health probes), 942200/942260 — exclude on selectors, not globally, where possible.
5. Switch to **Prevention**; keep a per-domain policy so one app's exclusions don't weaken another.

## 4. Custom rules (evaluated before managed, by priority)
- **Rate limit**: `--rule-type RateLimitRule --rate-limit-threshold 300 --rate-limit-duration 1` (per client IP + socket by default, 1 or 5 min windows) on `/login` and `/api/*` — `Block` or `Log`.
- **Geo**: `--match-variable RemoteAddr --operator GeoMatch --values GB IE --negate true --action Block` (allow-list countries) — remember `X-Forwarded-For` vs `RemoteAddr` via `SocketAddr` on AFD.
- **Bot Manager** (AFD Premium): good bots allowed (search engines), bad bots (known signatures) blocked, unknown logged/challenged (JS challenge on AFD).
- IP allow/deny lists: `IPMatch` with CIDRs (hundreds of entries per rule; split across rules beyond the per-rule cap).
- `Allow` action on a custom rule skips managed rules — use for trusted scanners/partner IPs, and for the health-check path.

## 5. DDoS
- Every public IP gets **basic infrastructure DDoS** (platform-level, no telemetry, no SLA).
- **DDoS Network Protection**: plan resource (~fixed monthly, covers 100 public IPs across subscriptions in the tenant), VNet-level, adaptive tuning per IP, attack metrics/alerts (`Under DDoS attack or not`, `Inbound packets dropped DDoS`), mitigation reports and flow logs, cost protection credit, **DDoS Rapid Response** team during an active attack, and WAF discount. Enable per VNet: `az network vnet update --ddos-protection true --ddos-protection-plan <plan-id>`.
- **DDoS IP Protection**: per public IP SKU (`az network public-ip update --ddos-protection-mode Enabled`), same mitigation, cheaper for < 15 IPs; no DRR/cost protection.
- Front Door/AFD endpoints are protected by AFD's own global DDoS; attach a plan to the origin VNet regardless for the hub public IPs (firewall, VPN gateway, AGW).
- Test: Microsoft-approved partners (BreakingPoint Cloud, Red Button, RedWolf) for simulation — self-run floods violate terms.

## Gotchas
- WAF on AFD evaluates **before** routing; a block looks like a 403 from `Microsoft-Azure-Application-Gateway/v2`/AFD, not your app — the `trackingReference`/`X-Azure-Ref` header correlates to the log.
- Exclusions apply to the *value* of the selected variable; the rule still evaluates the key name — some rules need a key-name exclusion too (`RequestArgKeys`).
- Switching DRS versions resets rule overrides; redo exclusions.
- Rate limiting on AFD is per POP region approximately, not globally exact — budget ±.
- A WAF in Prevention with request-body check and a 128 KB cap will block file uploads unless `maxRequestBodySizeInKb`/file upload limits are raised (AGW up to 4 GB file upload separately).
- DDoS Network Protection plan cost is tenant-shared: one plan, many VNets; two plans doubles the bill.

## Verify
- [ ] `curl "https://www.example.com/?q=1'%20OR%20'1'='1"` returns 403 in Prevention; log row shows `action=Block`, rule 942100, anomaly score ≥ 5.
- [ ] Legit API traffic for 24 h after enabling Prevention shows 0 Blocks for known-good clients (compare against the Detection week).
- [ ] Rate-limit rule: 400 requests/min from one IP to `/login` → 429/403 after the threshold.
- [ ] VNet shows `ddosProtectionPlan` set; public IP metric `Under DDoS attack` exists (value 0).
