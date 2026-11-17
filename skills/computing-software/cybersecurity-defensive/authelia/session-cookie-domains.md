---
id: computing-software.cybersecurity-defensive.authelia.session-cookie-domains
name: session-cookie-domains
category: computing-software
field: cybersecurity-defensive
product: authelia
tags: [authelia, session, cookies, authelia-url, multi-domain, public-suffix-list, sso]
level: practitioner
status: docs-checked
description: "Configure Authelia session.cookies per protected domain with authelia_url, default redirection, and the cookie-domain rules browsers and the public suffix list impose."
sources:
  - https://www.authelia.com/configuration/session/introduction/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Authelia authorises access with a session cookie, and `session.cookies` lists each domain it serves. A domain not listed is denied.

```yaml
session:
  secret: '<SESSION_SECRET>'
  cookies:
    - domain: 'example.com'
      authelia_url: 'https://auth.example.com'
      default_redirection_url: 'https://www.example.com'
      name: 'authelia_session'
      same_site: 'lax'
      inactivity: '5m'
      expiration: '1h'
      remember_me: '1d'
```

The `domain` value must:

1. Be a normal domain (hostname only, no port) for which a public CA would issue certificates. TLS is a strict requirement.
2. Be a valid suffix of, or exactly match, the hostname of `authelia_url`.
3. Contain at least one period.
4. Not exactly equal a public suffix such as `duckdns.org`; use `example.duckdns.org`. Browsers refuse to set cookies on public suffixes, so two sibling subdomains of one suffix cannot share a cookie.
5. Not be a special-use name like `localhost`.

Top-level `name`, `same_site`, `inactivity`, `expiration` and `remember_me` are defaults inherited by each cookie entry. `same_site: lax` is generally the best choice; `none` is discouraged and `strict` fails in many setups.

The list can hold several cookie domain entries with individual settings. Each entry's `authelia_url` is required, is the root URL of the Authelia portal for that domain, must use `https://`, and must include the path if Authelia is served from a subpath. `default_redirection_url` is optional, must use `https://` and must differ from `authelia_url`.

Check: log in on the portal and confirm the cookie appears with the expected `Domain` attribute in browser developer tools.

## Checked

2026-11-08. Read the full Authelia Session configuration page. Confirmed the cookie domain rules, authelia_url and default_redirection_url requirements, the SameSite guidance and the inheritance of top-level defaults. Replaced the unsourced one-entry-per-parent-domain advice with the documented requirements.

Method: documentation only; no commands were run.
