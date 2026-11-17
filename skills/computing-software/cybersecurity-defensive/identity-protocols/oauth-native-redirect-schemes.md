---
id: computing-software.cybersecurity-defensive.identity-protocols.oauth-native-redirect-schemes
name: oauth-native-redirect-schemes
category: computing-software
field: cybersecurity-defensive
product: identity-protocols
tags: [oauth-native-redirect-schemes, oauth-native-apps, rfc8252, native-app, loopback, claimed-https, custom-scheme, universal-links, identity-protocols]
level: practitioner
status: docs-checked
description: "Choose a native redirect: claimed https links (app links, universal links), loopback IP with random port, or private-use URI scheme with reverse domain."
sources:
  - https://www.rfc-editor.org/rfc/rfc8252
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Native app redirect options

Goal: return the code to the right app.

Options (RFC 8252 Section 7; native apps MAY use whichever suits them, taking platform details into account):
1. Claimed `https` scheme redirect (Section 7.2, for example Android App Links and iOS Universal Links): the operating system guarantees the destination app's identity to the AS, so native apps SHOULD use it over the other options where available.
2. Loopback interface (Section 7.3): `http://127.0.0.1:{port}/{path}` for IPv4 and `http://[::1]:{port}/{path}` for IPv6. The AS MUST allow any port at request time (the client takes an ephemeral port). Clients SHOULD NOT assume an IP version and are RECOMMENDED to try binding both. Using `localhost` is NOT RECOMMENDED because the IP literal avoids inadvertently listening on network interfaces and is not affected by name resolution.
3. Private-use URI scheme (Section 7.1): the scheme MUST be based on a domain name the developer controls, in reverse order, for example `com.example.app`.

Gotchas:
- Multiple apps can typically register the same private-use scheme; the AS must support PKCE for native clients, and public native apps MUST implement it (Sections 6 and 8.1) so an intercepting app cannot redeem the code.
- Embedded web-views are not allowed for authorization (see oauth-native-external-user-agent).
- Native apps are public clients and MUST be registered as such (Section 8.4), except where per-instance secrets are provisioned with dynamic client registration.

Verify: register the same scheme in a test app and confirm PKCE prevents it from using the code.

## Checked

Date: 2026-11-02. Confirmed in RFC 8252 Sections 7.1, 7.2, 7.3, 8.1, 8.4, 8.12. Removed as not stated there: "listen only on the loopback interface; close after one request", `/callback` path, "not interceptable" wording, the strict preference ranking beyond the claimed-https SHOULD.

Method: documentation only; no commands were run.
