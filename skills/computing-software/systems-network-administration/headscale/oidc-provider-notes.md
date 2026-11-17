---
id: computing-software.systems-network-administration.headscale.oidc-provider-notes
name: oidc-provider-notes
category: computing-software
field: systems-network-administration
product: headscale
tags: [headscale, keycloak, google, entra, kanidm, authentik, authelia]
level: advanced
status: docs-checked
description: "Provider-specific Headscale OIDC settings and quirks for Google, Microsoft Entra ID, Keycloak, Kanidm, Authentik and Authelia."
sources:
  - https://raw.githubusercontent.com/juanfont/headscale/main/docs/ref/oidc.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OIDC provider notes

Redirect URI for all providers: `https://headscale.example.com/oidc/callback`.

- **Authelia and Authentik**: fully supported. For Authentik leave the `Encryption Key` field unset; JSON Web Encryption is not supported.
- **Google**: issuer `https://accounts.google.com`. The `preferred_username` claim is not sent when the `profile` scope is requested, so the username stays blank. Create an OAuth client ID with application type "Web Application". Google has a verification process for users outside your domain; without a domain or for outside users you can add emails manually in the Google Console.
- **Microsoft Entra ID**: needs an App Registration with correct scopes and redirect URI. Issuer `https://login.microsoftonline.com/<tenant-UUID>/v2.0`. Optional `extra_params`: `domain_hint: example.com`, `prompt: select_account`. Groups filter uses scope `["openid", "profile", "email"]` and group IDs.
- **Keycloak**: allowed-groups needs a `groups` client scope with a Group Membership mapper on UserInfo, type `Default`.
- **Kanidm**: group names use the full SPN (`headscale_users@sso.example.com`). By default it sends the full SPN as `preferred_username`; to send the short name run:

```
kanidm system oauth2 prefer-short-username <client name>
```

## Gotcha

With Google the Headscale username is blank. With Kanidm the default SPN-style username (`alice@sso.example.com`) can be confusing; once short names are configured the username is `alice` and is referred to as `alice@` in the policy.

## Checked

2026-11-04. Confirmed against the Headscale OIDC page, identity provider specific configuration section (Authelia, Authentik, Google, Kanidm, Keycloak, Microsoft Entra ID). Removed the claim that these usernames break policies and the advice to check `headscale users list`, which the page does not state.

Method: documentation only; no commands were run.
