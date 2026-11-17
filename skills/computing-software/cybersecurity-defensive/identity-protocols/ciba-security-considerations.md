---
id: computing-software.cybersecurity-defensive.identity-protocols.ciba-security-considerations
name: ciba-security-considerations
category: computing-software
field: cybersecurity-defensive
product: identity-protocols
tags: [ciba-security-considerations, oidc-ciba, ciba, consent, authentication-device, identity-protocols]
level: sme
status: docs-checked
description: "Harden CIBA: signed login_hint_token, auth_req_id entropy, binding_message, user_code, polling interval, push-mode and id_token_hint cautions."
sources:
  - https://openid.net/specs/openid-client-initiated-backchannel-authentication-core-1_0.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CIBA security considerations

Goal: reduce misuse of the backchannel flow, where the user approves on an authentication device (AD) a request started from a separate consumption device.

What the spec says (section 14 unless noted):
- The `login_hint_token` SHOULD be digitally signed by its issuer, so the OP can authenticate the sender of the hint and rogue clients cannot harvest user identifiers.
- The OP SHOULD check that the registered `backchannel_client_notification_endpoint` is in the client's administrative authority, or results go to the wrong client.
- `id_token_hint` cannot follow normal JWT expiry rules: an expired ID token may still be accepted as a hint for some reasonable period. The OP should confirm it issued the token, that the requesting client is in `aud`, and verify the signature, but key rotation limits how long that is possible. The spec suggests an OP may skip signature checks and accept only ID tokens with pairwise subject identifiers, then verify the client was issued that identifier (or shares its sector identifier).
- Push mode delivers tokens straight to the client notification endpoint, so protect that endpoint and its registration. The ID token must carry hashes of the access token, refresh token and the `auth_req_id` so the client can detect tampering. Consider sender-constrained access tokens for push delivery.
- Context metadata (for example consumption-device geolocation compared with the AD) may help but is neither required nor defined.
- Privacy (section 15): avoid static global identifiers such as phone number or email as hints; alternatives are an ID token with a pairwise identifier, a single-use identifier passed from the AD to the consumption device, or a discovery service returning an encrypted `login_hint_token`.

Request parameters relevant to abuse:
- `auth_req_id` MUST have at least 128 bits of entropy (160 recommended); the OP MUST check it was issued to the requesting client, else return `invalid_grant`.
- `binding_message` SHOULD let the user tell the AD and consumption-device transactions are the same, for example a random value of reasonable entropy.
- `user_code` (optional secret known to the user, advertised via `backchannel_user_code_parameter_supported`) authorises sending a request to the user's device; error codes are `missing_user_code` and `invalid_user_code`.
- `requested_expiry` lets the client ask for the `auth_req_id` lifetime; the OP MAY use it.
- Polling must not be more frequent than the OP's `interval`; on `slow_down` increase it by at least 5 seconds; a client that polls too fast may get `invalid_request`.

Gotchas:
- Rate-limiting per user and requiring local biometric or PIN approval on the AD are sensible controls, but this specification does not mandate them.

Verify: send an `auth_req_id` issued to client A from client B and expect `invalid_grant`.

## Checked

Method: 2026-11-09 docs-only; read CIBA Core 1.0 sections 14 and 15 in full and the definitions of auth_req_id, binding_message, user_code, requested_expiry, interval and the error section by search. Removed unsourced numbers (120 s expiry), single-use auth_req_id and push-bombing mitigations.
