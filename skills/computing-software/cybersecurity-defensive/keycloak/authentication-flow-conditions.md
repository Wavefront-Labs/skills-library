---
id: computing-software.cybersecurity-defensive.keycloak.authentication-flow-conditions
name: authentication-flow-conditions
category: computing-software
field: cybersecurity-defensive
product: keycloak
tags: [cybersecurity-defensive, keycloak, conditions, condition-user-role, condition-user-attribute, conditional-2fa]
level: practitioner
status: docs-checked
description: "Use Keycloak flow conditions (user role, user configured, user attribute, sub-flow executed, client scope, credential) with Allow and Deny Access for conditional 2FA."
sources:
  - https://github.com/keycloak/keycloak/blob/main/docs/documentation/server_admin/topics/authentication/conditions.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# authentication flow conditions
Condition executions can only live inside a Conditional sub-flow. If all conditions evaluate true the sub-flow acts as Required and the next executions run; if any is false the whole sub-flow is treated as Disabled.

Conditions:
- **Condition - User Role**: true if the user has the role in the *User role* field (with an *Alias*). Application roles use `appname.approle`, for example `myapp.myrole`.
- **Condition - User Configured**: true if the other executions in the flow are configured for the user (the page's example is the OTP form).
- **Condition - User Attribute**: fields *Alias*, *Attribute name*, *Expected attribute value*, *Include group attributes* (checks joined groups; can affect performance) and *Negate output* (attribute should not be present).
- **Condition - sub-flow executed**: *Flow name* (required) and *Check result*: `executed` is true when that sub-flow ran with output success; `not-executed` is the negation.
- **Condition - client scope**: *Client scope name* (required) and *Negate output*. A default client scope of the requesting client is true; an optional scope is true only if the client sent it in the login request (for example the OIDC `scope` parameter).
- **Condition - credential**: *Credentials* list and *Included*; true if any listed credential was used (Included true), or if none was used (Included false).

Access control executions: **Allow Access** always succeeds (not configurable). **Deny Access** always denies; set an *Alias* and an *Error message*, plain text or a property key from the login theme `messages_en.properties` (for example `deny-role1 = You do not have required role!`); blank uses the default property `access-denied`. Example: a Conditional sub-flow with Condition - User Role plus Deny Access.

2FA patterns, based on the default browser flow's Conditional 2FA sub-flow (OTP Form on, WebAuthn and Recovery Codes disabled by default):
- All alternative: OTP, WebAuthn and Recovery Codes as Alternative inside a Condition - User Configured sub-flow; if the user has no 2FA credential the login still succeeds.
- Deny access if no 2FA: after the 2FA sub-flow add a sub-flow with Condition - sub-flow executed set to `not-executed` for it, followed by Deny Access.
- OTP default: same, but make the OTP Form Required so users with no 2FA must set up OTP to continue.

## Checked
2026-11-03. Confirmed against server_admin/topics/authentication/conditions.adoc. Removed: the admin-role mandatory-2FA recipe and the gotchas (empty conditional sub-flow, negation, enrolment) which are not on the page, and the Verify step; added the missing conditions and the three 2FA examples.
Method: documentation only; no commands were run.
