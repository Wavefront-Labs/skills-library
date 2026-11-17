---
id: computing-software.cybersecurity-defensive.identity-protocols.oauth-native-external-user-agent
name: oauth-native-external-user-agent
category: computing-software
field: cybersecurity-defensive
product: identity-protocols
tags: [oauth-native-external-user-agent, oauth-native-apps, webview, system-browser, asweb-authenticationsession, custom-tabs, external-user-agent, identity-protocols]
level: practitioner
status: docs-checked
description: "Use the system browser or in-app browser tabs for OAuth in native apps, and avoid embedded webviews that expose credentials and break SSO."
sources:
  - https://www.rfc-editor.org/rfc/rfc8252
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# External user agent versus embedded webviews

Goal: authenticate in a context the app cannot read.

Method (RFC 8252): use an external user agent, the system browser or an in-app browser tab, not an embedded user-agent. RFC 8252 Appendix B names `SFSafariViewController` and its successor `SFAuthenticationSession` on iOS and Custom Tabs on Android, and the "AppAuth pattern" libraries (AppAuth) implement it. Benefits stated there: the host app cannot copy user credentials and cookies, the browser's existing authentication session enables single sign-on, and the user does not authenticate from scratch in each app.

Gotchas:
- Native apps MUST NOT use embedded user-agents (typically web-views) for authorization requests (Section 8.12): the host app can capture credentials, and entering credentials there trains users to do so without validating the page.
- Platform APIs change; RFC 8252 says its implementation details (Appendix B) are accurate only at the time of publication, so check current Android and iOS documentation.

Verify: confirm the login runs in the system browser or an in-app browser tab, not a web-view.

## Checked

Date: 2026-11-02. Confirmed in RFC 8252 Sections 6, 8.12 and Appendix B. Removed as not stated there: `ASWebAuthenticationSession`, `prefersEphemeralWebBrowserSession`, claims that Google blocks web-views, cancel-handling advice, `state` check advice, WebAuthn and password manager claims.

Method: documentation only; no commands were run.
