---
id: computing-software.cloud-infrastructure-engineering.azure.application-gateway-waf-per-site-and-per-uri-policies
name: application-gateway-waf-per-site-and-per-uri-policies
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, waf, application-gateway, per-site-policy, per-uri-policy, waf-policy-association]
level: advanced
status: docs-checked
description: "Scope Application Gateway WAF policies globally, per listener (per-site) and per path rule (per-URI), and know which policy wins and how to deploy the associations."
sources: ["https://learn.microsoft.com/azure/web-application-firewall/ag/per-site-policies", "https://learn.microsoft.com/azure/web-application-firewall/ag/policy-overview", "https://learn.microsoft.com/cli/azure/network/application-gateway/waf-policy"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Per-site and per-URI WAF policies on Application Gateway

**Goal:** give one gateway that fronts many apps a different WAF posture per hostname or path without running several gateways.

## Association levels (most specific wins)
| Level | Attach to | Typical use |
|---|---|---|
| Global | The gateway (`firewallPolicy` on the AppGW resource) | Baseline for everything |
| Per-site | An HTTP listener (`httpListeners[].firewallPolicy`) | Different rule set / exclusions per hostname |
| Per-URI | A path rule in a path-based routing rule (`urlPathMaps[].pathRules[].firewallPolicy`) | Stricter or looser rules on `/api/*`, `/upload/*` |

The most specific policy takes precedence: a listener's policy takes effect for just that listener, and the global policy
still applies to listeners and path rules with no policy of their own. A policy holds all WAF settings (exclusions, custom
rules, managed rules), so design each scoped policy to be complete rather than a delta.

## Deploy
```bash
az network application-gateway waf-policy create -g rg -n wafp-api --type OWASP --version <ruleset-version>
az network application-gateway waf-policy policy-setting update -g rg --policy-name wafp-api \
  --mode Prevention --state Enabled
# attach to a listener
az network application-gateway http-listener update -g rg --gateway-name agw -n lst-api \
  --waf-policy /subscriptions/<sub>/resourceGroups/rg/providers/Microsoft.Network/ApplicationGatewayWebApplicationFirewallPolicies/wafp-api
# attach to a path rule
az network application-gateway url-path-map rule create -g rg --gateway-name agw --path-map-name pm1 \
  -n upload --paths "/upload/*" --address-pool pool-up --http-settings hs-up --waf-policy <policy-id>
```
Bicep: set `firewallPolicy: { id: wafApi.id }` on the listener or path rule object inside the `applicationGateways` resource.

## Rules
- Policy associations are supported only on the Application Gateway WAF_v2 SKU.
- A policy must be associated to take effect, and can be associated with any combination of gateways, listeners and
  path-based rules; there is no limit on the number of policies.
- Per-site needs a distinct listener per site; per-URI needs a path-based rule.

## Verify
- [ ] `az network application-gateway show -g rg -n agw --query "httpListeners[].{n:name,p:firewallPolicy.id}"` shows the intended mapping.
- [ ] A test request to each scoped listener or path is handled by the intended policy (check WAF logs and the policy's mode).

## Checked
2026-10-28. Confirmed in Learn WAF policy-overview and per-site-policies: global, per-site (listener) and per-URI (path rule)
association, most specific policy takes precedence, WAF_v2-only support, no limit on the number of policies, and the
`az network application-gateway waf-policy` command and its --type and --version options. check_commands found the CLI
commands valid. Removed: the 'policies do not merge' absolute, ruleset version 3.2, body size values, the portal upgrade tip,
the limits-page advice (contradicted by 'no limit'), bot manager copy advice and the policyScope log field names.
Method: documentation only; no commands were run.
