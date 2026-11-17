---
id: computing-software.cybersecurity-defensive.application-security.webhook-security
name: webhook-security
category: computing-software
field: cybersecurity-defensive
product: application-security
tags: [api-security, webhook-security, hmac-signature, replay-protection, ssrf, standard-webhooks, timing-safe-compare]
level: practitioner
status: docs-checked
description: "Secure webhooks both ways: verify HMAC signatures with timestamps and constant-time compare when receiving; prevent SSRF and sign payloads when sending."
sources: ["https://github.com/standard-webhooks/standard-webhooks/blob/main/spec/standard-webhooks.md", "https://docs.github.com/en/webhooks/using-webhooks/validating-webhook-deliveries", "https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Webhook security

Webhooks are HTTP requests from an unknown source, so verifying their authenticity is a requirement for any secure
implementation.

## Receiving webhooks
1. **Verify the signature** before processing. Compute it over the exact bytes that were sent. Parsing the body as
   JSON and serialising it again is a common failure: serialisation can differ and the signature will not match.
2. **GitHub**: the `X-Hub-Signature-256` header holds `sha256=` followed by the HMAC hex digest, computed from your
   webhook secret and the payload. Treat the payload as UTF-8. Use a high-entropy random secret and store it securely;
   never hardcode it or push it to a repository. GitHub's test vector: secret `It's a Secret to Everybody` with
   payload `Hello, World!` gives `sha256=757107ea0eb2509fc211221cce984b8a37570b6d7586c22c46f4379c8b043e17`.
3. **Standard Webhooks** (v1.0.0): headers `webhook-id`, `webhook-timestamp` (integer unix seconds) and
   `webhook-signature` (a space-delimited list of signatures, each prefixed `v1,` for HMAC-SHA256 or `v1a,` for
   ed25519). The signed content is `msg_id.timestamp.payload`. Try each listed signature until one verifies; the list
   supports zero-downtime secret rotation.
4. **Compare in constant time**: never a plain `==`; GitHub names `secure_compare` or `crypto.timingSafeEqual`, and
   Standard Webhooks warns that a non-constant-time compare enables timing attacks.
5. **Replay protection**: check that `webhook-timestamp` is within an allowed tolerance of the current time, and use
   `webhook-id` as an idempotency key so an event is processed once (the spec suggests, as an example, keeping IDs for
   5 minutes).
6. Signing keys should be unique per endpoint; for asymmetric schemes consumers keep a trust list of public keys and
   must not read the public key from a request header.

## Sending webhooks
- **Sign every delivery** with the Standard Webhooks scheme above; the spec prefers asymmetric signatures unless you
  control both producer and consumer. The secret for HMAC should be random, 24 to 64 bytes.
- **SSRF**: customers can register any URL, so protect internal networks. The spec recommends sending through a
  filtering proxy (it names smokescreen) and running webhook workers in a private subnet that cannot reach internal
  services. OWASP adds: prefer allowlists; if you must use a deny list, it is bypass-prone, so cover private, loopback,
  link-local, IPv6 unique-local and link-local ranges and cloud metadata addresses (for example `169.254.169.254`);
  normalise IPv4-mapped and NAT64 IPv6 forms before comparing; disable redirect following; and connect only to the
  validated address, since a second DNS lookup between validation and connection allows DNS rebinding.
- Treat only `2xx` as success; treat `3xx` as failure rather than following redirects; disable the endpoint on
  `410 Gone`; throttle on `429`, `502` and `504`; honour `retry-after`. Retry with exponential backoff and jitter over
  multiple days, and disable and notify the consumer for persistent failure. A request timeout of 15 to 30 seconds is
  recommended.
- Consider HTTPS-only endpoints: signatures prove authenticity but do not encrypt the payload.
- Thin payloads (identifiers only) keep data access auditable; keep payloads small (the spec suggests under 20 kb).

## Verify
Valid signature accepted, modified body rejected, old timestamp rejected, duplicate `webhook-id` ignored; for
senders, registering a loopback or metadata address as an endpoint is refused.

## Checked
Method: docs-checked 2026-11-09 against the Standard Webhooks specification v1.0.0 (raw spec markdown, read in
full), the GitHub "Validating webhook deliveries" page (read up to the code examples) and the OWASP SSRF Prevention
Cheat Sheet (allowlist, deny-list and normalisation sections). Removed unconfirmed claims: the hand-written Python
verifier, the Stripe header format, the GitHub meta IP allowlist, "respond fast and process asynchronously" and the
secrets-manager and two-active-secrets wording.
