---
id: computing-software.cybersecurity-defensive.keycloak.workflows-security-considerations
name: workflows-security-considerations
category: computing-software
field: cybersecurity-defensive
product: keycloak
tags: [cybersecurity-defensive, keycloak, workflows, self-registration, user-attributes, privilege-escalation]
level: practitioner
status: docs-checked
description: "Avoid privilege escalation in Keycloak workflows by controlling who can write attributes that conditions check before privileged steps."
sources:
  - https://github.com/keycloak/keycloak/blob/main/docs/documentation/server_admin/topics/workflows/security-considerations.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# workflows security considerations
When designing workflows, understand the trust boundaries between the event that triggers a workflow, the conditions that decide whether it runs, and the steps it executes. A misconfigured workflow can let users trigger privileged actions on themselves without administrator involvement; this matters most when self-registration is enabled.

Conditions such as `has-user-attribute` evaluate attributes stored on the user, and steps such as `grant-role` and `join-group` perform privileged actions on the same user, so the safety of the workflow depends on who can write the attribute the condition checks. Unsafe example from the docs:
```yaml
name: Onboarding gold members
on: user-created
if: has-user-attribute(membership=gold)
steps:
  - uses: grant-role
    with:
      role: gold-member
```
If end users can write `membership` (for example through a registration form), a self-registering user can set `membership=gold` and receive the `gold-member` role with no administrator review.

Controls:
- Unmanaged attributes: when the *Unmanaged Attributes* policy in realm settings is `Enabled`, Keycloak persists any attribute submitted during registration, even if not in the user profile. Avoid `Enabled`; prefer `Disabled` (default) or `Admin can edit`.
- Managed attributes: an attribute is still user-writable if its *Who can edit* permission includes User. For attributes used in conditions of privileged steps, restrict *Who can edit* to Admin (*Realm Settings* > *User Profile* > *Attributes*).
- Workflows triggered by user-initiated events such as `user-created` run with the triggering user as the target of every step, and attributes set at registration are present when the condition is evaluated. If self-registration is disabled and users are created only by administrators, the risk described does not apply.

## Checked
2026-11-03. Confirmed against server_admin/topics/workflows/security-considerations.adoc. Removed (not on the page): the "prefer conditions based on verified email domain" advice, a duplicate gotcha and the Verify step.
Method: documentation only; no commands were run.
