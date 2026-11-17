---
id: computing-software.cloud-infrastructure-engineering.ansible.controller-teams-local-users-and-superusers
name: controller-teams-local-users-and-superusers
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, controller-rbac, team-roles, superuser, organizations]
level: practitioner
status: docs-checked
description: "Manage controller teams and team role grants, local users, system administrators and auditors, and password and session policies, preferring team-based access."
sources: ["https://docs.redhat.com/en/documentation/red_hat_ansible_automation_platform/2.5/html-single/access_management_and_authentication/", "https://docs.redhat.com/en/documentation/red_hat_ansible_automation_platform/2.5/html-single/using_automation_execution/", "https://docs.ansible.com/projects/awx/en/latest/rest_api/authentication.html", "https://github.com/redhat-cop/infra.aap_configuration"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Teams, local users and superusers

## Teams first
Grant roles to **teams**, never to individual users: joiners/leavers become team membership changes (ideally driven by LDAP/SAML group mapping).
```yaml
controller_teams:              # infra.aap_configuration role inputs
  - name: web-ops
    organization: Platform
controller_roles:
  - team: web-ops
    role: execute
    job_templates: [Deploy web, Restart web]
  - team: web-ops
    role: use
    inventories: [Production]
    credentials: [prod-ssh]
```
Team-level roles on the organization (organization admin and resource-admin roles) scale better than per-object grants.

## User types
| Type | Power |
|---|---|
| Normal user | only what roles grant |
| System auditor | read-only everywhere (compliance, support) |
| System administrator (superuser) | everything, including settings and all orgs |
In AAP 2.5 these are platform-level (gateway) and the organization admin role covers org scope.

## Superusers
- Keep 2-3 break-glass local superuser accounts with strong passwords in a vault; everyday admins log in via SSO with org admin roles.
- Audit superusers via the activity stream (filter on user changes) or the users API (`is_superuser` field).

## Local user policy
Session policy is configurable (`SESSION_COOKIE_AGE` for session expiry; session limits cap simultaneous
sessions per user or IP). Once SSO works, keep at least one other authenticator or a break-glass local
admin enabled — the gateway documentation requires another enabled authenticator before disabling one.

## Gotchas
- Users mapped by LDAP/SAML get team membership overwritten at each login if `remove: true` in maps.
- Deleting a user does not delete objects they created; ownership is by organization.

## Verify
```bash
awx teams list -f human; awx roles list -f human
```

## Checked

- 2026-10-31: team-based role assignment, System Auditor and System Administrator (superuser)
permissions, `SESSION_COOKIE_AGE` and per-user/IP session limits, and the guidance to keep another
authenticator enabled confirmed in AAP 2.5 Access management and authentication, Using automation
execution and the AWX REST API authentication page. `controller_teams`/`controller_roles` role
names confirmed in the redhat-cop roles listing; `awx teams list`, `awx roles list` confirmed in
the AWX CLI reference.
- Removed: the `ansible.controller.team`/`role` module examples (replaced with the confirmed role
  inputs), the `--is_superuser` CLI flag form and the `LOCAL_PASSWORD_MIN_LENGTH`/`SESSIONS_PER_USER`/
  `DISABLE_LOCAL_AUTH` setting names (not in the current documentation).
Method: documentation only; no commands were run.
