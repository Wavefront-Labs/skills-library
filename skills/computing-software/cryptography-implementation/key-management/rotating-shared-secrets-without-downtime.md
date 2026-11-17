---
id: computing-software.cryptography-implementation.key-management.rotating-shared-secrets-without-downtime
name: rotating-shared-secrets-without-downtime
category: computing-software
field: cryptography-implementation
product: key-management
tags: [key-management, cryptography-implementation, shared-secret-rotation, hmac, webhook-secret, api-keys, database-credentials, dual-secret, key-rotation, zero-downtime]
level: practitioner
status: gated
description: "Rotate shared HMAC, webhook, API and database secrets with dual-secret acceptance, staged rollout and confirmation, including peers that support only one secret."
sources: ["https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html", "https://docs.aws.amazon.com/secretsmanager/latest/userguide/rotating-secrets.html", "https://docs.stripe.com/webhooks#roll-endpoint-secrets"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Rotating shared secrets without downtime

Shared secrets have two holders; rotation must keep both sides working while the secret changes.

## Pattern A: verifier accepts two secrets
1. Generate the new secret; add it to the verifier's accepted set (`[new, old]`).
2. Give it to the producer; producer switches.
3. Watch metrics for signatures validated by `old`; when zero for a full traffic cycle, remove `old`.

```python
def verify(msg, sig, secrets):
    return any(hmac.compare_digest(hmac.new(s, msg, "sha256").hexdigest(), sig) for s in secrets)
```

## Pattern B: provider-managed roll
Stripe lets you "roll" an endpoint signing secret and either expire the old one immediately or delay its expiry for up to 24 hours; both secrets are active during that time (Stripe webhook docs). Configure your verifier with both before rolling.

## Pattern C: peer accepts only one secret
Some peers (single API key slot, legacy database users) cannot hold two. Options:
- Two credentials (alternating users): create user B with the new secret, switch the app to B, then rotate A for
  next time (AWS Secrets Manager "alternating users" strategy (gated: unconfirmed, source is paywalled or blocked)).
- Brief maintenance window with retry on auth failure.

## Database passwords
- AWS Secrets Manager single-user rotation (gated: unconfirmed, source is paywalled or blocked) changes the password and relies on clients refetching on auth failure;
  alternating-users avoids the gap.
- Clients must refetch the secret on auth failure instead of caching forever.

## Gotchas
- Logging which secret version validated each request is how you know when to retire the old one.
- Rotating after a leak: skip overlap; revoke immediately.
- Secrets embedded in mobile apps or firmware cannot be rotated quickly; avoid shared secrets there.

## Verify
- [ ] Rotation drill shows zero failed requests.
- [ ] Old secret rejected after retirement.
