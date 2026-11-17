---
id: computing-software.cybersecurity-defensive.identity-protocols.oidc-back-channel-logout
name: oidc-back-channel-logout
category: computing-software
field: cybersecurity-defensive
product: identity-protocols
tags: [oidc-back-channel-logout, oidc-logout, back-channel-logout, logout_token, backchannel_logout_uri, events, sid, identity-protocols]
level: advanced
status: docs-checked
description: "Receive server-to-server logout tokens at backchannel_logout_uri: validate the logout JWT events claim, sid and sub, and end the session."
sources:
  - https://openid.net/specs/openid-connect-backchannel-1_0.html
  - https://openid.net/specs/openid-connect-frontchannel-1_0.html
  - https://openid.net/specs/openid-connect-rpinitiated-1_0.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Back-Channel Logout and logout tokens

Goal: reliably end RP sessions without the browser.

Method: the RP registers `backchannel_logout_uri` (and optionally `backchannel_logout_session_required`). The OP POSTs `logout_token=<JWT>` (form encoded) to it. The RP must validate the token:
- decrypt it if encrypted; verify the signature as for ID Tokens (`alg` `none` must not be used);
- validate `iss`, `aud`, `iat` and `exp` as for ID Tokens;
- `events` contains the member `http://schemas.openid.net/event/backchannel-logout`;
- `sub`, `sid` or both is present; **no `nonce`** claim;
- optionally check the same `jti` was not received recently, and that `iss`/`sub`/`sid` match an ID Token from a current or recent session.
If validation fails, reject with HTTP 400. If it succeeds, clear the identified sessions (already logged out counts as success) and respond 200 (an OP should also accept 204). The response should carry `Cache-Control: no-store`.

Gotchas:
- If no `sid` is present, all sessions of the user identified by `iss` and `sub` are to be logged out, so keep a session index by `sid` and `sub` to find them.
- Logout tokens should be explicitly typed with the `typ` header `logout+jwt`.
- Refresh tokens issued without `offline_access` to a session being logged out should be revoked; those with `offline_access` normally should not be.
- Back-channel logout is not known to be affected by browsers blocking third-party content.

Verify: post a valid signed test token, then one containing `nonce`; the second must be rejected with 400.

## Checked
2026-11-02. Confirmed against OpenID Connect Back-Channel Logout 1.0 (sections 2.2 to 2.8, 3, 4) and Front-Channel Logout 1.0 section 4.1. Removed: "`exp` (short)", "jti not seen before" as mandatory (the spec makes it optional), the stateless JWT cookie revocation list advice, and the claim that the endpoint must not need a user session.
Method: documentation only; no commands were run.
