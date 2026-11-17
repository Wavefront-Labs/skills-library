---
id: computing-software.collaboration-platform-administration.vikunja.oidc-login-troubleshooting
name: oidc-login-troubleshooting
category: computing-software
field: collaboration-platform-administration
product: vikunja
tags: [vikunja, well-known-openid-configuration, redirecttoprovider, extra-settings-links, oidc-mobile-webview, oidc-proxy]
level: advanced
status: docs-checked
description: "Debug Vikunja OIDC problems: ignored endpoint URLs, discovery document checks, proxy routing, mobile webview failures, auto-redirect and custom settings links."
sources:
  - https://raw.githubusercontent.com/go-vikunja/website/main/src/content/docs/setup/openid.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Endpoint URLs ignored: Vikunja fetches `<authurl>/.well-known/openid-configuration` and the returned URLs win over anything configured. For a non-standard port or proxied provider, fix the discovery document. Check it:

```
curl https://your-provider/.well-known/openid-configuration | jq .
```

Verify `authorization_endpoint`, `token_endpoint` and `userinfo_endpoint`.

Provider unreachable through a proxy (from 2.7.0): OIDC requests use the outgoing proxy. When `outgoingrequests.proxyurl` is set this includes internal providers. Make the proxy reach the provider, or use `HTTPS_PROXY` with the provider host in `NO_PROXY`.

Mobile apps use an embedded webview that may mishandle cookies; "State does not match" is typically a webview session issue. "Login with frontend" is recommended.

Auto-redirect: append `?redirectToProvider=<provider-id>` to the login URL. With one provider, `?redirectToProvider`, `=true` or `=1` also work.

Custom settings links: an `extra_settings_links` claim in the ID token, an object of keys each with `text` and `url`, adds links to the user settings navigation.

With the provider option `requireavailability: true` (default false, per config-raw.json) Vikunja crashes if it cannot reach the provider at startup, so container orchestrators such as Kubernetes can restart it.

## Checked

2026-11-04: checked against the OpenID page troubleshooting and auto-login sections, and config-raw.json (requireavailability). Reworded the `requireavailability` line to the documented behaviour.

Method: documentation only; no commands were run.
