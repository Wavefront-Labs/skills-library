---
id: computing-software.cryptography-implementation.applied-cryptography.verifying-hmac-signed-webhooks
name: verifying-hmac-signed-webhooks
category: computing-software
field: cryptography-implementation
product: applied-cryptography
tags: [applied-cryptography, cryptography-implementation, webhook-signature-verification, webhooks, hmac, hmac-sha256, replay-protection, constant-time-compare, stripe, github, slack]
level: practitioner
status: verified
description: "Verify Stripe, GitHub, Slack-style HMAC webhook signatures: raw body handling, timestamp tolerance, constant-time compare, secret rotation and replay defence."
sources: ["https://docs.stripe.com/webhooks#verify-manually", "https://docs.github.com/en/webhooks/using-webhooks/validating-webhook-deliveries", "https://api.slack.com/authentication/verifying-requests-from-slack"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Verifying HMAC-signed webhooks

## Provider formats
| Provider | Header | Signed string | Algorithm |
|---|---|---|---|
| Stripe | `Stripe-Signature: t=<unix>,v1=<hex>[,v1=...]` | `"{t}.{raw_body}"` | HMAC-SHA256, default tolerance 300 s |
| GitHub | `X-Hub-Signature-256: sha256=<hex>` | `raw_body` | HMAC-SHA256 (no timestamp) |
| Slack | `X-Slack-Signature: v0=<hex>`, `X-Slack-Request-Timestamp` | `"v0:{ts}:{raw_body}"` | HMAC-SHA256, reject if the timestamp differs from local time by more than five minutes |

## Verification code (Python, provider-agnostic shape)
```python
import hmac, hashlib, time
def verify(secret: bytes, raw_body: bytes, ts: str, sig_hex_list: list[str], tolerance=300) -> bool:
    if abs(time.time() - int(ts)) > tolerance:
        return False
    expected = hmac.new(secret, f"{ts}.".encode() + raw_body, hashlib.sha256).hexdigest().encode()
    return any(hmac.compare_digest(expected, s.encode()) for s in sig_hex_list)
```

Run: valid, tampered body, 400 s old timestamp and multi-signature cases behave as expected. Compare
**bytes**: `hmac.compare_digest(str, str)` raises `TypeError` on a non-ASCII header value (run), which would
turn a forged header into a 500. Also wrap `int(ts)` so a non-numeric timestamp returns False; upper-case hex
does not match lower-case (run). GitHub's documented signature is `X-Hub-Signature-256: sha256=<hex>` over the
payload (GitHub docs): strip the `sha256=` prefix or include it in the expected string.

## Rules
1. **Use the raw bytes.** Verify before JSON parsing; re-serialising changes whitespace and key order. In Express use
   `express.raw({type: 'application/json'})` on the webhook route (run with express 4: `req.body` is a Buffer of the
   exact 10 bytes sent, while `express.json()` gives a parsed object); in Flask `request.get_data()` (run: returns the
   exact string, double spaces and trailing newline included).
2. **Constant-time compare** (`hmac.compare_digest` on bytes, `crypto.timingSafeEqual` with equal lengths, `MessageDigest.isEqual` in Java).
3. **Timestamp window** to limit replay; additionally store event IDs and drop duplicates (deliveries are retried).
4. **Accept multiple signatures** during secret rotation (Stripe sends one `v1` per active secret); keep old and new
   secrets valid for an overlap window, then remove the old one.
5. Return 2xx quickly and process asynchronously; signature failure returns 400 with no detail.

## Gotchas
- Proxies or frameworks that decompress, re-encode or strip a trailing newline break signatures.
- Hex case: compare lowercase hex to lowercase hex.
- GitHub's legacy `X-Hub-Signature` uses HMAC-SHA1 and is "only included for legacy purposes" (GitHub docs); ignore it.
- Do not log the secret or full signature on failure.

## Verify
- [ ] Unit test with a captured real delivery passes; one-byte body change fails.
- [ ] Request older than the tolerance is rejected.
- [ ] Rotation test: both secrets accepted during overlap, old rejected after.
