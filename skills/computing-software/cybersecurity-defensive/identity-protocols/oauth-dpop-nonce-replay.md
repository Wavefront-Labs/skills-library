---
id: computing-software.cybersecurity-defensive.identity-protocols.oauth-dpop-nonce-replay
name: oauth-dpop-nonce-replay
category: computing-software
field: cybersecurity-defensive
product: identity-protocols
tags: [oauth-dpop-nonce-replay, oauth-dpop, dpop-nonce, use_dpop_nonce, replay, jti-cache, iat-window, identity-protocols]
level: advanced
status: docs-checked
description: "Handle use_dpop_nonce challenges: server-provided nonces, DPoP-Nonce headers, jti caches and iat windows to limit proof pre-generation and replay."
sources:
  - https://www.rfc-editor.org/rfc/rfc9449
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DPoP server nonces and replay protection

Goal: stop attackers pre-computing or replaying proofs.

Method (server): accept proofs only for a limited time (on the order of seconds or minutes) and, where feasible, store each `jti` for that window to reject reuse; to require a nonce, an authorization server replies 400 (a resource server 401 with `WWW-Authenticate: DPoP`) with error `use_dpop_nonce` and a `DPoP-Nonce` header; nonces must be unpredictable, and servers keep a window of recent nonces.
Method (client): on `use_dpop_nonce` retry with the supplied value in the proof's `nonce` claim, and keep using the latest nonce until the server supplies a new one (AS and RS provide nonces separately).

Gotchas:
- Without nonces, an attacker with brief access to the client can mint proofs with future `iat` for later use; nonces bound lifetime.
- Single-use `jti` checks may be infeasible when several servers behind one endpoint share no state (RFC 9449 section 11.1).

Verify: send a proof with an old nonce and expect rejection, optionally with a fresh DPoP-Nonce header.

## Checked

2026-11-02. Confirmed against RFC 9449 sections 8, 8.2, 9, 11.1 and 11.2 (`use_dpop_nonce`, 400 versus 401, unpredictable nonces, retry with the nonce claim, `jti` storage, pre-generated proofs). Removed: the few-minutes figures, nonce rotation interval, shared-secret advice and the retry-loop remark.
Method: documentation only; no commands were run.
