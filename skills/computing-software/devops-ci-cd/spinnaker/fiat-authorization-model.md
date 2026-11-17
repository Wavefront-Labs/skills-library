---
id: computing-software.devops-ci-cd.spinnaker.fiat-authorization-model
name: fiat-authorization-model
category: computing-software
field: devops-ci-cd
product: spinnaker
tags: [fiat, authorization, rbac, permissions, roles, accounts, applications, execute]
level: practitioner
status: docs-checked
description: "Reason about Fiat permissions: open-by-default resources, READ/WRITE/EXECUTE on roles, account versus application access, executeFallback and what typical actions need."
sources:
  - https://spinnaker.io/docs/setup/other_config/security/authorization/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Fiat is Spinnaker's authorization service. It is **disabled by default**. It needs authentication working in Gate, an external role provider (Google Groups, GitHub organization, LDAP, a SAML IdP that includes groups, or OAuth2 with groups in the claims) and fiat enabled in `spinnaker.yml`.

**Rules to remember:**
- The model is **open by default**: a resource that defines no permissions is unrestricted. An unrestricted account lets any Spinnaker user deploy a new application there; an unrestricted application can be deployed by anyone into another account.
- Every permission is granted to a **role**, never directly to a user. Super admin is also granted to a role.
- Accounts hold many applications and applications span accounts; access to one does not imply the other.

**Accounts** have `READ` (view resources) and `WRITE` (change them). Set them with a `permissions` block on the account listing roles under `READ` and `WRITE`. WRITE does not imply READ, so always add READ to any WRITE grant.

**Applications** have `READ`, `WRITE` and `EXECUTE`. By default `READ` also grants `EXECUTE`; to make only `WRITE` imply it, set `fiat.executeFallback: 'WRITE'` in `fiat-local.yml`.

**Examples:** delete a load balancer needs `WRITE` on the account; update a pipeline needs `WRITE` on the app; running a pipeline needs only `EXECUTE`; run a pipeline in app X deploying to account Y needs `EXECUTE` on X and `WRITE` on Y.

**Role providers:** a YAML file, GitHub Teams, Google Groups, LDAP, and SAML groups (also OIDC OAuth) as `EXTERNAL` roles.

Automated triggers against protected resources need pipeline permissions (automatic on-demand service accounts) or a Fiat service account. SAML roles are fixed at login and cannot change until the user re-authenticates.

## Checked

2026-11-04. Open-by-default, role-only grants, account and application permission rules, executeFallback, examples and the provider list were confirmed on the Authorization (RBAC) page. Removed: the `hal config provider account edit` permission flags, the Front50 S3/GCS requirement and the since-1.14 claim (none on the page).

Method: documentation only; no commands were run.
