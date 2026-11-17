---
id: computing-software.networking-hardware-and-wireless.f5-big-ip.local-traffic-policies
name: local-traffic-policies
category: computing-software
field: networking-hardware-and-wireless
product: f5-big-ip
tags: [networking-hardware-and-wireless, f5-big-ip, ltm-policy, local-traffic-policy, policy-rules]
level: practitioner
status: draft
description: "Replace simple iRules with BIG-IP local traffic policies for host/URI routing, redirects and header edits."
sources:
  - https://techdocs.f5.com/en-us/bigip-15-1-0/big-ip-local-traffic-manager-implementations.html
  - https://clouddocs.f5.com/api/irules/HTTP__uri.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Local traffic policies (LTM policies)

```
tmsh create ltm policy pol_route strategy first-match requires add { http } controls add { forwarding } rules add {
  api { conditions add { 0 { http-host host values { api.example.com } } } actions add { 0 { forward select pool pool_api } } }
  http2https { conditions add { 0 { tcp address matches values { 0.0.0.0/0 } } } actions add { 0 { http-redirect location "tcl:https://[HTTP::host][HTTP::uri]" } } }
}
tmsh modify ltm virtual vs_web policies add { pol_route }
tmsh publish ltm policy pol_route
```
- Policies are drafted before use: edit the `Drafts/` copy and `publish`. A policy that is `legacy` bypasses the draft model (confirm).
- `strategy first-match` stops at the first matching rule; `all-match` applies every matching rule; `best-match` picks the most specific.
- `requires` lists the data the policy needs (`http`, `client-ssl`, `tcp`), and `controls` the action types (`forwarding`, `request-adjustment`, `ssl-persistence`, `waf`...). A control you did not declare cannot be used.
- Policies run on a compiled engine and cost less CPU than iRules, but their expressions are limited. Use iRules only for logic that policies cannot express.
- Gotcha: a policy needs a matching profile (the HTTP profile for HTTP conditions); `publish` fails with "requires" errors otherwise.

Verify: `tmsh list ltm policy pol_route`, `tmsh show ltm policy pol_route` for per-rule hit counters, and `curl -H 'Host: api.example.com' http://vip/`.
