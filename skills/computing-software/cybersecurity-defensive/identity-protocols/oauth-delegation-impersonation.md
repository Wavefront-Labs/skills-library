---
id: computing-software.cybersecurity-defensive.identity-protocols.oauth-delegation-impersonation
name: oauth-delegation-impersonation
category: computing-software
field: cybersecurity-defensive
product: identity-protocols
tags: [oauth-delegation-impersonation, oauth-token-exchange, act-claim, may_act, delegation, impersonation, on-behalf-of, actor-chain, identity-protocols]
level: sme
status: docs-checked
description: "Model on-behalf-of access with the act claim for delegation, may_act authorisation and impersonation, and carry the actor chain for audit."
sources:
  - https://www.rfc-editor.org/rfc/rfc8693
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Delegation versus impersonation (act and may_act)

Goal: record who is acting for whom.

- Impersonation: A is given B's rights and is indistinguishable from B in that context; a token request with only a `subject_token` (no `actor_token`) can only have impersonation semantics.
- Delegation: A keeps its own identity and acts representing B. The request carries `subject_token` (the party on whose behalf) and `actor_token` (the party receiving the rights). A composite token may express this with the JWT `act` claim, a JSON object identifying the actor (for example `iss` and `sub`). Whether and when a composite token is issued is at the authorization server's discretion.
- `may_act` in the subject token states that a party is authorized to become the actor for the subject; the server can use it to decide whether the client (or the actor token's party) may engage in the requested delegation or impersonation.

Method: for access control the consumer of a token MUST consider only the top-level claims and the party identified as the current actor by the outermost `act` claim.

Gotchas:
- Nested `act` claims are prior actors, informational only, and not to be used in access decisions.
- Non-identity claims such as `exp`, `nbf` and `aud` inside `act` or `may_act` are not meaningful.
- `act` and `may_act` also appear as top-level members of an introspection response with the same semantics.
- Delegation and impersonation raise abuse risk; the RFC suggests `scope` and limited token lifetime to mitigate.

Verify: decode the exchanged token and confirm the act chain.

## Checked
2026-11-02. Confirmed against RFC 8693 sections 1.1, 4.1, 4.4 and 5. Removed: "prefer delegation", "authorise using the intersection of user and actor permissions", the `sub`/`act` shape as a guaranteed output, and the Entra on-behalf-of note (not documented by the RFC).
Method: documentation only; no commands were run.
