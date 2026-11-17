---
id: computing-software.web-development.node-express.safe-outbound-webhooks-and-link-previews
name: safe-outbound-webhooks-and-link-previews
category: computing-software
field: web-development
product: node-express
tags: [ssrf, server-side-request-forgery, outbound-webhooks, link-preview, webhook-delivery, hmac-signature, egress-proxy, unfurling]
level: practitioner
status: docs-checked
description: "Building user-configured webhooks and link unfurling safely: SSRF-safe delivery workers, timeouts/size caps, HMAC signing, retries and disabling bad endpoints."
sources:
  - https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html
  - https://github.com/stripe/smokescreen
  - https://github.com/standard-webhooks/standard-webhooks/blob/main/spec/standard-webhooks.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Safe outbound webhooks and link previews

**Goal:** features where users give you a URL to call or preview don't become an SSRF or DoS vector, and receivers can trust your calls.

## 1. Delivery architecture
- Deliver from a **separate worker** (queue job), never in the request thread.
- Route all outbound traffic through an egress proxy that only permits public IPs (Smokescreen) or a network segment with no internal routes.
- Validate URL at registration **and** at each delivery (DNS changes).

## 2. Request limits
- `https:` only, ports 443 (maybe 80/8443) only.
- Use a short connect timeout and total timeout (for example 3 s and 10 s), cap the response body (for example 64 KB, then abort) and don't follow redirects for webhooks; these values are examples to tune.
- Don't send internal headers/cookies; set a clear `User-Agent: ExampleWebhooks/1.0`.

## 3. Signing so receivers can verify
Standard Webhooks style:
```js
const id = crypto.randomUUID(), ts = Math.floor(Date.now()/1000);
const sig = crypto.createHmac('sha256', endpointSecret).update(`${id}.${ts}.${body}`).digest('base64');
headers = { 'webhook-id': id, 'webhook-timestamp': String(ts), 'webhook-signature': `v1,${sig}` };
```
Per-endpoint secret (the spec uses 24 to 64 random bytes, serialised as base64 with a `whsec_` prefix), rotate with overlap; receivers check that `webhook-timestamp` is within an allowed tolerance, use `webhook-id` as an idempotency key and compare signatures in constant time.

## 4. Retries and abuse
Exponential backoff with jitter over several days (the spec's example schedule runs to about 75 hours), idempotent `webhook-id`; auto-disable endpoints after sustained failures and notify the owner. Per-tenant rate limits so one customer can't use you to flood a third party.

## 5. Link previews (unfurling)
Fetch with the same SSRF-safe client, accept only `text/html` up to a small size, parse only `<head>` meta (`og:title`, `og:image`), then fetch the `og:image` through the same safe path (or an image proxy) - the image URL is a second SSRF vector. Cache results; never render fetched HTML.

## Verify
- [ ] Registering `http://169.254.169.254/` or a hostname that later resolves internally fails at delivery.
- [ ] Slow-loris endpoint is cut off at the timeout; huge response truncated.
- [ ] Receiver sample code verifies signatures; replay older than the tolerance is rejected.

## Checked

2026-10-25 against the Standard Webhooks spec 1.0.0, the Smokescreen README and OWASP Cheat Sheet Series (OWASP/CheatSheetSeries, commit of 2026-10-24). Confirmed: Standard Webhooks headers webhook-id, webhook-timestamp and webhook-signature, signature prefix v1, signed content msg_id.timestamp.payload; verifiers use a constant-time comparison, check the timestamp tolerance and use webhook-id as an idempotency key; the spec recommends retries with exponential backoff and jitter over multiple days, then notifying the consumer and disabling the endpoint; Smokescreen resolves hostnames and only connects to publicly routable IPs, with allow/deny ACLs; OWASP SSRF cheat sheet allow-list versus any-address cases.

Method: documentation only; no commands were run.
