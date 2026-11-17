---
id: computing-software.cybersecurity-defensive.keycloak.post-broker-login-flow
name: post-broker-login-flow
category: computing-software
field: cybersecurity-defensive
product: keycloak
tags: [cybersecurity-defensive, keycloak, post-login-flow, idp-2fa, identity-brokering, otp]
level: practitioner
status: docs-checked
description: "Require an extra step such as OTP after every login through an external identity provider using a Keycloak post login flow."
sources:
  - https://github.com/keycloak/keycloak/blob/main/docs/documentation/server_admin/topics/identity-broker/post-login-flow.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# post broker login flow
A post login flow triggers additional authentication actions after every login with a particular identity provider. The docs example: trigger 2-factor authentication after every login through Facebook because Facebook does not provide it during its own login. Set up the authentication flow with the needed steps, then set it as *Post login flow* when configuring the identity provider.

Examples in the docs:
- Single method: a flow with one 2FA authenticator such as OTP. A user without OTP set up is asked to configure it at the first login with the identity provider.
- Multiple methods as ALTERNATIVE: make sure a user without any 2FA is asked to set one up, either by making one 2FA method REQUIRED in the First login flow (works if all users are registered by identity provider login), or by wrapping the 2FA methods as ALTERNATIVE in a conditional sub-flow (such as `2FA`) and adding another conditional sub-flow (such as `OTP if no 2FA`) that runs only if the previous one did not and asks the user to add a method. A similar configuration is in the Conditions section of the Authentication flows chapter.
- Dedicated clients: with `Condition - client scope`, require OTP after identity provider login only when a given client scope (the docs use `foo`) is requested. The client must have the scope as default or optional; if optional, the flow runs only when the client requests the scope (for example through the OIDC `scope` parameter).

## Checked
2026-11-03. Confirmed against server_admin/topics/identity-broker/post-login-flow.adoc. Removed (not on the page): the "every login vs first login flow" comparison, the flow type claim, the gotchas about password form steps and errors, and the Verify step.
Method: documentation only; no commands were run.
