---
id: computing-software.cybersecurity-defensive.keycloak.forgot-password-reset-flow
name: forgot-password-reset-flow
category: computing-software
field: cybersecurity-defensive
product: keycloak
tags: [cybersecurity-defensive, keycloak, forgot-password, reset-credentials, reset-flow, force-login]
level: practitioner
status: docs-checked
description: "Enable Keycloak forgot password and tune the Reset Credentials flow: OTP reset, force-login-after-reset values, and direct redirect from an application."
sources:
  - https://github.com/keycloak/keycloak/blob/main/docs/documentation/server_admin/topics/login-settings/forgot-password.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# forgot password reset flow
Enabling *Forgot password* lets users reset credentials if they forget a password or lose their OTP generator.

Enable: *Realm settings* > *Login* tab > toggle *Forgot password* ON; a "Forgot Password?" link appears on login pages. Set *Host* and *From* on the *Email* tab so Keycloak can send the reset email. The user enters a username or email and receives a link. The email text is configurable (see the developer guide). Also make sure *Update Password* is enabled under *Authentication* > *Required actions*.

Default behaviour: after the link, Keycloak asks for a new password, and asks to reconfigure the OTP generator if one was set up. For security the flow forces federated users to log in again after the reset, and keeps internal-database users logged in if the same authentication session (same browser) is used.

Change it under *Authentication* > *Flows* tab > *Reset Credentials* flow:
- To skip OTP reset, set the `Reset - Conditional OTP` sub-flow requirement to Disabled.
- To change the force login behaviour, click the *Send Reset Email* settings icon, define an *Alias*, and choose *Force login after reset*: `true` always forces re-authentication, `false` keeps the user logged in if the same browser was used, `only-federated` (the default) forces login only for federated users.

An OIDC application can redirect directly to the Reset credentials screen by slightly changing the initial authentication request URL (described in the guide's client flows section, not covered here).

## Checked
2026-11-03. Confirmed against server_admin/topics/login-settings/forgot-password.adoc. Removed: the "lowers reset strength", account-existence, action-token lifespan and email-address gotchas, and the Verify step with event names, none of which are on the page; added the three force-login values and the Email tab prerequisite.
Method: documentation only; no commands were run.
