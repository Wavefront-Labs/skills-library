---
id: computing-software.cybersecurity-defensive.zitadel.default-redirect-uri
name: default-redirect-uri
category: computing-software
field: cybersecurity-defensive
product: zitadel
tags: [zitadel, redirect-uri, login, console, auth-request]
level: practitioner
status: docs-checked
description: "Set the instance Default Redirect URI so users who reach login without an OIDC request land in your app instead of the Management Console."
sources:
  - https://zitadel.com/docs/guides/manage/console/default-settings
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The Default Redirect URI is used when the context of the authentication request is lost, or when someone opens the login page directly with no OIDC flow. Normally an application starts login with an authorization request carrying a client id and a redirect URI that must match ZITADEL's configuration. Without that context ZITADEL needs somewhere to send the user.

Common situations without request context:

- The login was not called with an OIDC authorize request.
- The user bookmarked the login page and opened it directly.
- The user arrived from an email link, such as password reset or user initialization.

If you do not want end users to reach the Management Console after these flows, set your own default redirect URI. For the instance, change it at `https://${CUSTOM_DOMAIN}/ui/console/instance?id=login`.

The default value is `https://${CUSTOM_DOMAIN}/ui/console/`. A sensible replacement is your main application's home URL, so a person who finished a password reset email lands back in the product.

## Checked

2026-11-08. Read the default settings page in full; added the default value.

Method: documentation only; no commands were run.
