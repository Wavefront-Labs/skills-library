---
id: computing-software.cybersecurity-defensive.keycloak.client-secret-rotation-policy
name: client-secret-rotation-policy
category: computing-software
field: cybersecurity-defensive
product: keycloak
tags: [cybersecurity-defensive, keycloak, secret-rotation, client-policies, rotated-secret, executor]
level: practitioner
status: docs-checked
description: "Rotate Keycloak confidential client secrets through Client Policies: two concurrent secrets, expiration settings and when rotation actually happens."
sources:
  - https://github.com/keycloak/keycloak/blob/main/docs/documentation/server_admin/topics/clients/oidc/con-secret-rotation.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# client secret rotation policy
For clients with Confidential Client authentication, Keycloak can rotate client secrets through Client Policies, to reduce problems such as secret leakage. Once enabled, up to two secrets per client are active at once. A rotation generates a new main secret and the old main secret becomes the secondary secret with a new expiration date.

Settings (all in seconds, calculated at policy execution time):
- **Secret expiration**: expiration of the new secret, added to the secret creation date.
- **Rotated secret expiration**: remaining life of the old secret, added to the rotation date. Should always be smaller than Secret expiration. 0 removes the old secret immediately at rotation.
- **Remaining expiration time for rotation during update**: the period in which an update to a dynamic client should perform rotation.

Rules: rotation is not automatic and there is no background process. It needs an update action on the client: *Regenerate Secret* in the client's *Credentials* tab of the Admin Console, or the Admin REST API (which can also force rotation at any time). On an update, rotation happens when Secret expiration is earlier than the current date, and during a dynamic client registration update when the Remaining expiration time value matches the period between now and Secret expiration. For new clients, the behaviour applies automatically while the policy is active. For an existing client, update it after defining the policy.

The policy itself is a client profile with the secret rotation executor and a client policy that selects clients (see client-policies-profiles-and-executors for the building blocks).

## Checked
2026-11-03. Confirmed against server_admin/topics/clients/oidc/con-secret-rotation.adoc. Removed: the example second values, the step-by-step profile/policy procedure and the "invalid if at or above" gotcha (the page says "should" be smaller), and the Verify step.
Method: documentation only; no commands were run.
