---
id: computing-software.cloud-infrastructure-engineering.azure.waf-javascript-challenge-and-captcha-actions
name: waf-javascript-challenge-and-captcha-actions
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, waf, javascript-challenge, captcha, bot-protection, front-door, application-gateway, custom-rules]
level: advanced
status: docs-checked
description: "Use WAF JavaScript challenge and CAPTCHA actions on Front Door and Application Gateway, set cookie validity, and know the client and API limitations."
sources: ["https://learn.microsoft.com/azure/web-application-firewall/waf-javascript-challenge", "https://learn.microsoft.com/azure/web-application-firewall/afds/captcha-challenge", "https://learn.microsoft.com/azure/web-application-firewall/afds/waf-front-door-custom-rules"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# WAF JavaScript challenge and CAPTCHA

**Goal:** slow bots and scrapers with an invisible or interactive challenge instead of a hard block.

## Actions
| Action | Where | What the client sees |
|---|---|---|
| JavaScript challenge | Front Door Premium: custom rule action and Bot Manager 1.x ruleset. Application Gateway WAF: advanced bot protection (Learn marks the Application Gateway feature as PREVIEW) | Invisible challenge page for a few seconds while the browser computes; on success WAF treats the client as a non-bot and runs the remaining rules; failures are blocked |
| CAPTCHA | Front Door Premium | Interactive Microsoft CAPTCHA page; failures are blocked. Usage-based charges apply (see the Front Door pricing page) |

The challenge endpoint is public, but requests to it are not forwarded to the backend and do not count toward rate limiting.

## Validity
The policy setting sets the cookie lifetime: an integer between 5 and 1,440 minutes, default 30. After it expires the client is challenged again. Cookie names: `afd_azwaf_jsclearance` (JS challenge, Front Door), `appgw_azwaf_jsclearance` (Application Gateway), `afd_azwaf_captcha` (CAPTCHA, Front Door). Look up the exact policy property names in the current template or API reference rather than guessing them.

## Limitations (design around them)
- AJAX and API calls are not supported by either feature, so scope rules to HTML page routes. CAPTCHA does not support mobile apps.
- The first request that triggers the challenge is blocked if its POST body exceeds 64 KB on Front Door (128 KB on Application Gateway for the JS challenge).
- Designed for HTML resources; challenging embedded images, CSS or scripts is unsupported (the JS challenge lifts this after a prior successful challenge).
- Not supported on Internet Explorer; works on current Edge, Chrome, Firefox and Safari.
- CORS requests are challenged on every access attempt; the challenge is also reissued if the client IP changes.
- Application Gateway: the JS challenge action is not supported for rate limit custom rules during the preview, and Application Gateway for Containers WAF does not support it.

## Verify
- [ ] A browser passes the challenge and receives the clearance cookie; scripted clients (curl) are challenged or blocked on the scoped routes.
- [ ] API paths are not covered by the challenge rule.

## Checked
2026-10-31. Confirmed on the JavaScript challenge, CAPTCHA and Front Door custom rules Learn pages: availability, cookie names, 5-1,440 minute range and 30 minute default, POST body limits, browser and AJAX limitations, CORS and IP-change behaviour, Application Gateway preview and rate-limit restriction. Removed: the Bicep fragment and literal action/property names (the custom rules page lists only Allow, Block, Log, Redirect), "POST bodies not replayed", the HTTP 403 expectation, the log action names, the claim to combine rate limits with the challenge, and the iframe/privacy-browser looping claim.
Method: documentation only; no commands were run.
