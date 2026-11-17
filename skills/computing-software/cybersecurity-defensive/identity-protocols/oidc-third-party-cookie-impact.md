---
id: computing-software.cybersecurity-defensive.identity-protocols.oidc-third-party-cookie-impact
name: oidc-third-party-cookie-impact
category: computing-software
field: cybersecurity-defensive
product: identity-protocols
tags: [oidc-third-party-cookie-impact, oidc-session-management, third-party-cookies, itp, samesite, silent-auth, prompt-none, iframe, identity-protocols]
level: advanced
status: docs-checked
description: "Replace iframe-based session checks broken by third-party cookie blocking with silent prompt=none redirects, short sessions and back-channel logout."
sources:
  - https://openid.net/specs/openid-connect-session-1_0.html
  - https://openid.net/specs/openid-connect-frontchannel-1_0.html
  - https://openid.net/specs/openid-connect-backchannel-1_0.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Third-party cookie blocking and session sync

Goal: understand which OIDC session mechanisms break when browsers block third-party content.

Facts from the specs:
- Some user agents block third-party content (content from an origin different from the focused window) by default, including cookies and web storage APIs.
- Session Management: the OP iframe loaded in the RP page may lack its cookies or storage, so cookie-based implementations can return `changed` on every call and cause infinite re-authentication loops. The spec recommends defensive code that detects this and tells the user the RP logouts could not be done.
- Front-Channel Logout: the `frontchannel_logout_uri` rendered in the OP's iframe may be unable to access the RP's login state.
- Back-Channel Logout is not known to be affected.

Method:
- Prefer back-channel logout; use front-channel and session management only with defensive detection.
- When session management reports a change, the specs say to try a `prompt=none` request in an iframe with the old ID Token as `id_token_hint`; test it in browsers that block third-party content.

Gotchas:
- Behaviour differs by browser and changes over time ("the tracking prevention situation is fluid"); test each target browser.

Verify: test in a browser with third-party cookies blocked.

## Checked
2026-11-02. Confirmed against OpenID Connect Session Management 1.0 section 5.1, Front-Channel Logout 1.0 section 4.1 and Back-Channel Logout 1.0 section 4. Removed: backend-for-frontend, refresh-token rotation, same-site custom domain, SameSite/registrable-domain, Safari ITP and "silent iframe flows are hard to support" advice, none of which these specs state.
Method: documentation only; no commands were run.
