---
id: computing-software.collaboration-platform-administration.vikunja.outgoing-requests-proxy
name: outgoing-requests-proxy
category: computing-software
field: collaboration-platform-administration
product: vikunja
tags: [vikunja, outgoingrequests, forward-proxy, no-proxy, ssrf-protection, ssl-cert-dir, mole-proxy]
level: advanced
status: docs-checked
description: "Route Vikunja's outgoing HTTP (webhooks, OIDC, migrations, avatars) through a forward proxy, with SSRF protection, NO_PROXY behaviour and custom CA trust in Docker."
sources:
  - https://raw.githubusercontent.com/go-vikunja/website/main/src/content/docs/setup/outgoing-proxy.mdx
  - https://raw.githubusercontent.com/go-vikunja/vikunja/main/config-raw.json
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Available from 2.7.0. Through the proxy: webhooks, avatar downloads, Unsplash backgrounds, Todoist, Trello, Microsoft To Do and Planka migrations, OIDC discovery/token/userinfo/keys, and the Pro license check. SMTP and LDAP are not HTTP and bypass it.

Configure either way; the config option wins if both are set:
- Environment: `HTTPS_PROXY`, `HTTP_PROXY`, `NO_PROXY` (hosts, domain suffixes like `.internal`, CIDRs; localhost never proxied).
- Config: `outgoingrequests.proxyurl: "http://user:password@proxy.internal:3128"`. Or keep the password apart with `outgoingrequests.proxypassword` (username from the URL, else `vikunja`, as mole expects; ignored if the URL has a password).

The config option has no `NO_PROXY`, so even an internal OIDC provider goes via the proxy. An invalid proxy URL makes requests fail, not bypass.

SSRF: by default Vikunja refuses private, loopback and link-local targets. The connection to the proxy itself is exempt. Proxied requests are resolved by the proxy, so a generic proxy such as Squid will not block internal targets; use a filtering proxy like mole or deny internal networks if untrusted users can create webhooks or migrations. `outgoingrequests.allownonroutableips` lifts the check.

Custom CA: in Docker mount the CA and set `SSL_CERT_DIR` (adds to defaults); avoid `SSL_CERT_FILE`, which replaces them.

## Checked

2026-11-04. Confirmed against the Vikunja Outgoing requests through a proxy page (setup/outgoing-proxy): 2.7.0 availability, what goes through the proxy, environment and config options and precedence, NO_PROXY handling, proxypassword and the mole username, SSRF behaviour, the Squid warning and SSL_CERT_DIR advice. Nothing removed.

Method: documentation only; no commands were run.
