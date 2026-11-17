---
id: computing-software.cybersecurity-defensive.identity-protocols.oidc-check-session-iframe
name: oidc-check-session-iframe
category: computing-software
field: cybersecurity-defensive
product: identity-protocols
tags: [oidc-check-session-iframe, oidc-session-management, check_session_iframe, session_state, postmessage, session-management, identity-protocols]
level: advanced
status: docs-checked
description: "Monitor OP login state from the browser with check_session_iframe, session_state, postMessage and salt; understand the cookie-based design."
sources:
  - https://openid.net/specs/openid-connect-session-1_0.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# check_session_iframe and session_state

Goal: detect OP logout or user change at the RP without server round trips.

Method: when the OP supports session management, the authentication response includes `session_state` (an opaque string without spaces, based on a salted hash of client ID, origin URL and OP user-agent state). The RP loads an invisible OP iframe from the OP's `check_session_iframe`, and an RP iframe polls it with `postMessage`, sending `client_id + " " + session_state` at an interval suitable for the application; the OP iframe replies `unchanged`, `changed` or `error`. On `changed`, the RP should first try a `prompt=none` request in an iframe, sending the old ID Token as `id_token_hint`; if it gets an ID Token for the same user it updates the session state, otherwise it treats this as a logout.

Gotchas:
- Both iframes must enforce the expected origin of each message and reject others.
- The OP iframe needs OP cookies or storage inside an RP page; browsers blocking third-party content can make cookie-based implementations return `changed` every time, causing infinite re-authentication loops. The spec recommends defensive code to detect this.
- RPs must handle false-positive `changed` results silently.

Verify: check discovery for `check_session_iframe`; absent means the OP does not advertise it.

## Checked
2026-11-02. Confirmed against OpenID Connect Session Management 1.0 sections 2, 3, 3.1, 3.2, 4 and 5.1, and Discovery section 3 (metadata extended by Session Management). Removed: the "spec status is draft" and "many OPs dropped it" remarks, and the "spec suggests modest intervals" wording (the spec says an interval suitable for the application).
Method: documentation only; no commands were run.
