---
id: computing-software.software-engineering.api-design.webhook-delivery-and-signatures
name: webhook-delivery-and-signatures
category: computing-software
field: software-engineering
product: api-design
tags: [api-design, idempotency, webhooks, webhook-signatures, hmac, standard-webhooks, retries, replay-protection, ssrf, event-delivery]
level: practitioner
status: verified
description: "Design webhooks both sides: HMAC signing with timestamps, retries with backoff, idempotent receivers, fast 2xx acks, ordering, SSRF-safe delivery and endpoint management."
sources: ["https://www.standardwebhooks.com/", "https://github.com/standard-webhooks/standard-webhooks/blob/main/spec/standard-webhooks.md", "https://docs.stripe.com/webhooks", "https://docs.github.com/en/webhooks/using-webhooks/validating-webhook-deliveries"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Webhook delivery and signatures

**Goal:** event notifications to customers' HTTP endpoints that are authentic,
eventually delivered, and safe to process more than once.

## Payload and headers (Standard Webhooks shape)
```
POST /hooks HTTP/1.1
webhook-id: msg_2Kf...            # unique per message, stable across retries
webhook-timestamp: 1760611200     # unix seconds
webhook-signature: v1,base64(HMAC-SHA256(secret, id + "." + timestamp + "." + body))
content-type: application/json

{"type": "invoice.paid", "timestamp": "...", "data": {"id": "inv_123", ...}}
```
- Thin vs fat payloads: include the resource id and type; including full data saves a
  call but may be stale by the time it's processed. Many APIs send data and recommend
  re-fetching for critical decisions.
- Version the event schema; let customers pin a version.

## Sender responsibilities
- Sign every message; per-endpoint secrets; support rotation (send multiple
  signatures during overlap).
- Retry non-2xx and timeouts with exponential backoff over hours/days
  (e.g. 5s, 5m, 30m, 2h, 5h, 10h...), then mark failed and disable the endpoint after
  sustained failure, notifying the owner.
- Timeout: the Standard Webhooks spec recommends 15-30 s; treat 3xx as a failed delivery rather than following it (spec: following redirects adds load, update the URL instead); disable the endpoint on `410 Gone`.
- SSRF: customer-supplied URLs can point at internal addresses. Resolve DNS, block
  private/link-local/metadata ranges (169.254.169.254), and send from an isolated egress
  proxy.
- Provide a dashboard/API for delivery logs and manual replay.

Signing scheme checked against the Standard Webhooks spec: signed content is `msg_id.timestamp.payload`, header `webhook-signature` is space-delimited `v1,<base64>` entries (so rotation works by sending two), `v1a` marks asymmetric signatures, and secrets are serialised as base64 with a `whsec_` prefix (so base64-decode the part after the prefix to get the HMAC key bytes; the function below takes the key bytes). The spec example retry schedule is 5 s, 5 min, 30 min, 2 h, 5 h, 10 h, 14 h, 20 h, 24 h and it recommends jitter. The verify function below was run: a two-signature header passed, a tampered body, wrong secret and 10-minute-old timestamp were rejected.

## Receiver responsibilities
```python
def verify(secret: bytes, headers, body: bytes) -> None:
    ts = int(headers["webhook-timestamp"])
    if abs(time.time() - ts) > 300: raise Invalid("stale")          # replay window
    signed = f'{headers["webhook-id"]}.{ts}.'.encode() + body       # RAW body bytes
    expected = base64.b64encode(hmac.new(secret, signed, "sha256").digest()).decode()
    if not any(hmac.compare_digest("v1," + expected, s) for s in headers["webhook-signature"].split()):
        raise Invalid("signature")
```
- Verify on the RAW body before JSON parsing (re-serialised JSON won't match).
- Constant-time compare.
- Dedupe by `webhook-id` (store processed ids) because retries and at-least-once
  delivery produce duplicates.
- Ack fast: enqueue and return 2xx, process asynchronously; slow handlers cause
  timeouts and duplicate retries.
- Don't assume ordering; use timestamps/versions in data or re-fetch the resource.

## Verify
- [ ] Receiver rejects a tampered body, a wrong secret and a 10-minute-old timestamp.
- [ ] Sending the same message twice results in one side effect.
- [ ] Sender refuses endpoints resolving to private IP ranges.
