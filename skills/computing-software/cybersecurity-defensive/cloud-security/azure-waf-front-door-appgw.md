---
id: computing-software.cybersecurity-defensive.cloud-security.azure-waf-front-door-appgw
name: azure-waf-front-door-appgw
category: computing-software
field: cybersecurity-defensive
product: cloud-security
tags: [azure-waf, azure-front-door, application-gateway, waf-policy, default-rule-set, bot-protection, cloud-network-security]
level: practitioner
status: docs-checked
description: "Configure Azure WAF on Front Door and Application Gateway: managed rule sets, detection to prevention, exclusions, custom and rate-limit rules, origin lockdown."
sources: ["https://learn.microsoft.com/en-us/azure/web-application-firewall/afds/afds-overview", "https://learn.microsoft.com/en-us/azure/web-application-firewall/ag/ag-overview", "https://learn.microsoft.com/en-us/azure/web-application-firewall/afds/waf-front-door-exclusion", "https://learn.microsoft.com/en-us/azure/frontdoor/origin-security", "https://learn.microsoft.com/en-us/azure/web-application-firewall/afds/waf-front-door-monitor"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Azure Front Door and Application Gateway WAF

## Choose placement
- **Front Door WAF** (global edge): policy is replicated to all Microsoft edge locations; internet-facing apps, geo filtering, bot protection.
- **Application Gateway WAF** (regional): the gateway sits in your virtual network, so use it for regional inspection or apps behind private networking. A policy can be associated globally, per site or per URI.

## WAF policy
1. Managed rules: Front Door has the Azure-managed **Default Rule Set** (covers XSS, Java attacks, LFI, PHP injection, RCE, RFI, session fixation, SQL injection, protocol attackers) plus an optional bot protection rule set. Application Gateway supports **CRS 3.2**, 3.1 and 3.0 plus a Bot Manager rule set; CRS 3.2 or later runs the newer WAF engine.
2. Start new deployments in **Detection** mode (logs matches, blocks nothing), review the logs for a short period, add exceptions or custom rules, then switch to **Prevention**. On Application Gateway, prevention returns a 403 and closes the connection.
3. Exclusions (Front Door) are scoped by match variable: Request header name, Request cookie name, Query string args name, Request body POST args name, Request body JSON args name. Scope them narrowly to the rule or rule group that needs them.
4. Custom rules are evaluated before managed rules and consist of a match condition, a priority (lower number runs first) and an action. Front Door actions: Allow, Block, Log, Redirect and Anomaly score (Default Rule Set 2.0 or later). Application Gateway actions: Allow, Block, Log, Anomaly score. Controls include IP allow/block lists, geo-match, HTTP parameter matches, request method, size constraints and rate limiting.
5. Front Door **rate limiting** caps requests per client IP over a one-minute or five-minute window and can be combined with match conditions (for example a path); on Premium you can also group by country/region or ASN.

## Origin lockdown (critical)
WAF is bypassed if the origin is reachable directly. For Front Door:
- Prefer Private Link origins where possible.
- For public IP origins use both: IP filtering with the `AzureFrontDoor.Backend` service tag (never hard-code IPs, they change), and verifying the `X-Azure-FDID` header equals your Front Door profile ID, because other Azure customers share those IP addresses. Also allow Azure infrastructure addresses 168.63.129.16 and 169.254.169.254.
- On Application Gateway as origin, allow ports 80 and 443 only from the `AzureFrontDoor.Backend` tag, deny the Internet tag, and use a custom WAF rule to check `X-Azure-FDID`.
For Application Gateway directly, keep backends in private subnets with NSGs that allow only the gateway subnet.

## Logs
Send WAF logs to a storage account, event hub, Log Analytics or a partner solution via diagnostic settings (turn on logging in the Diagnostics section; Detection mode logs only if enabled). Front Door category `FrontDoorWebApplicationFirewallLog`; blocked requests:
`AzureDiagnostics | where ResourceProvider == "MICROSOFT.CDN" and Category == "FrontDoorWebApplicationFirewallLog" | where action_s == "Block"`
The `TrackingReference` field matches the `X-Azure-Ref` response header, so you can find one request.

## Verify
- [ ] Policy in Prevention mode; a test attack payload is blocked.
- [ ] Direct origin request without Front Door is rejected.

## Checked
Checked 2026-11-09 against the five Microsoft Learn pages in `sources` (WAF modes, actions, rule sets, custom rules, exclusion match variables, rate limiting, origin security, monitoring query). Removed unconfirmed claims: specific "DRS 2.1" rule set versions, the exact rate limit example, the Application Gateway log category name and the 1-2 week detection period. The Front Door rate-limit page was fetched but not read line by line; only the overview's rate limiting description is relied on.
Method: documentation only; no commands were run.
