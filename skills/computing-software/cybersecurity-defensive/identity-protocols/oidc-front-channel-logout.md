---
id: computing-software.cybersecurity-defensive.identity-protocols.oidc-front-channel-logout
name: oidc-front-channel-logout
category: computing-software
field: cybersecurity-defensive
product: identity-protocols
tags: [oidc-front-channel-logout, oidc-logout, front-channel-logout, frontchannel_logout_uri, sid, iframe, frontchannel_logout_session_required, identity-protocols]
level: advanced
status: docs-checked
description: "Receive OP logout notifications in the browser via an iframe to frontchannel_logout_uri, with iss and sid parameters and their cookie limits."
sources:
  - https://openid.net/specs/openid-connect-frontchannel-1_0.html
  - https://openid.net/specs/openid-connect-backchannel-1_0.html
  - https://openid.net/specs/openid-connect-rpinitiated-1_0.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Front-Channel Logout

Goal: clear RP sessions via the browser when the OP ends a session.

Method: the RP registers `frontchannel_logout_uri` and optionally `frontchannel_logout_session_required`. At logout the OP renders an `<iframe src="frontchannel_logout_uri">` for each logged-in RP, appending `iss` and `sid` query parameters when the RP requires them. The RP clears state tied to the identified session (cookies and local storage; already logged out counts as success), and may check that `iss` and `sid` match an ID Token from a current or recent session, ignoring the request if not. Discovery advertises `frontchannel_logout_supported` and `frontchannel_logout_session_supported`; the `sid` claim also appears in ID Tokens when supported.

Gotchas:
- Browsers blocking third-party content can stop the iframe from accessing the RP's login state; the spec recommends defensive code to detect this and notify the user.
- Back-channel logout is not known to be affected by that blocking, so use it in addition where possible.
- An RP that is also an OP can serve nested iframes to log out its downstream sessions.

Verify: log out from the OP and check that the RP requests to the front-channel URI clear the session.

## Checked
2026-11-02. Confirmed against OpenID Connect Front-Channel Logout 1.0 (sections 2, 3, 4.1) and Back-Channel Logout 1.0 section 4.1/Session Management 5.1 wording. Removed: SameSite and frame-ancestors/X-Frame-Options remarks, "best effort / tab closing" remark, which the spec does not state.
Method: documentation only; no commands were run.
