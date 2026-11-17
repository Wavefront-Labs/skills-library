---
id: computing-software.cloud-infrastructure-engineering.ansible.controller-organizations-teams-and-rbac
name: controller-organizations-teams-and-rbac
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, awx, automation-controller, awx-rbac, controller-rbac, organizations, teams, users, roles, execute-role, admin-role, use-role, read-role, ldap-team-mapping, saml, oidc, sso, platform-gateway, system-auditor, least-privilege, role-definitions, aap-2-5]
level: practitioner
status: docs-checked
description: "Model AWX/controller access: organizations as tenants, teams mapped from SSO/LDAP groups, object roles (Admin/Use/Execute/Read), auditors, and least-privilege patterns."
sources: ["https://docs.redhat.com/en/documentation/red_hat_ansible_automation_platform/2.5/html-single/access_management_and_authentication/", "https://docs.redhat.com/en/documentation/red_hat_ansible_automation_platform/2.5/html-single/using_automation_execution/", "https://github.com/redhat-cop/infra.aap_configuration"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Controller organizations, teams and RBAC

**Goal:** a developer can launch the deploy template for their app and read its
logs, but cannot see prod credentials, edit the playbook source or run anything
against another team's inventory.

## 1. The model
- **Organization** = tenant boundary. Projects, inventories, credentials (optionally), job templates, teams and EEs belong to one org. Start with one org per business unit or environment, not per app.
- **Team** = a named group of users inside an org; roles are granted to teams, almost never to individual users.
- **Object roles** (per resource):
  | Role | Grants |
  |---|---|
  | Admin | everything on the object, including deleting and re-sharing |
  | Use | reference the object in another (use a credential/inventory/project in a template) **without** seeing its secrets |
  | Execute | launch a job/workflow template |
  | Update | sync a project / update an inventory source |
  | Read | view |
  | Ad hoc (inventory) | run ad hoc commands against it |
  | Approve (workflow) | approve approval nodes |
- **Org-level roles**: Admin, Execute, Project Admin, Inventory Admin, Credential Admin, Workflow Admin, Notification Admin, Job Template Admin, Execution Environment Admin, Auditor, Member, Read.
- **System roles**: System Administrator (superuser), System Auditor (read everything).
Roles inherit downward: org Admin implies Admin on every object in it; team roles flow to members.

## 2. A least-privilege layout that works
```
Org: platform
  Team: platform-admins      -> Org Admin
  Team: app-a-devs           -> Execute on JT "app-a deploy (stage)", Read on inventory "stage"
  Team: app-a-ops            -> Execute on "app-a deploy (prod)", Approve on workflow "app-a release", Read on inventory "prod"
  Team: auditors             -> System Auditor (via platform-level role)
Credentials: "prod ssh" owned by platform-admins; job template "app-a deploy (prod)" has it attached.
```
Devs launch prod via the template but never hold `Use` on the prod credential or `Admin` on the
template, so they cannot swap in a different playbook or inventory. `prompt on launch` on a
template is what re-opens that door — leave it off on prod templates (or restrict with surveys).

## 3. Mapping from SSO
AAP 2.5: authentication lives in the **platform gateway** (Authentication → Authenticators:
LDAP, SAML, OIDC/Keycloak, Azure AD, GitHub, RADIUS, TACACS+). Each authenticator has **maps**:
"if user is in group `cn=app-a-devs,ou=groups,dc=example` → add to Team `app-a-devs` in Org `platform`",
with organization/team/superuser map types and Remove Users so group removal revokes (the documented
behaviour: with Remove Users disabled, `is_superuser` is never removed). Legacy controller releases
(pre-2.5) used per-backend settings for the same idea. Disable local login for humans once SSO works;
keep one local break-glass admin in a vault.

## 4. Automate it
```yaml
- infra.aap_configuration.controller_organizations: {name: platform, default_environment: ee-platform}
- infra.aap_configuration.controller_teams: {name: app-a-devs, organization: platform}
- infra.aap_configuration.controller_roles:
    team: app-a-devs
    job_templates: ["app-a deploy (stage)"]
    role: execute
```
(The roles drive the certified `ansible.controller`/upstream `awx.awx` modules.) Keep this in git; the UI is for reading.

## 5. Audit
Activity Stream (per object and global) records who changed what; System Auditor is the role for
security teams (a system-level auditor can see everything without change rights). `awx roles list`
for a quick dump of grants; review orphaned direct user grants quarterly.

## Gotchas
- `Use` on a credential lets a user attach it to **any** template they can admin — pair with no `Admin` on templates.
- Org Admins can see every credential in their org that is org-owned; make credentials user-owned (private) only for personal tokens.
- Deleting a team does not remove its users' memberships elsewhere; deleting a user cascades their owned credentials.
- `Execute` on a template whose inventory has `prompt on launch` lets the user pick any inventory they can `Use` — the inventory `Use` role is the real gate.
- Superusers bypass everything; keep the list at 2-3 accounts and alert on changes via the activity stream/webhook.
- The API exposes role filtering such as `role_level=admin_role`; UI role labels and API field names differ — check the object's roles list in the API.

## Verify
- [ ] Log in as a member of `app-a-devs`: can launch the stage template, cannot open the prod credential or edit the template.
- [ ] Removing a user from the SSO group and logging in again drops the team membership (map `remove: true`).
- [ ] `awx roles list` shows no direct user grants outside the break-glass admin.

## Checked

- 2026-10-31: the RBAC model (roles granted per resource and via teams, member/admin/auditor types,
  System Auditor, System Administrator, template access via Team/User Access tabs) and gateway
  authenticator maps (organization/team mapping, remove-users behaviour, is_superuser) confirmed
  in AAP 2.5 Using automation execution and Access management and authentication. `infra.aap_configuration`
  role names `controller_organizations`, `controller_teams`, `controller_roles` confirmed in the
  redhat-cop roles listing; `awx roles list` confirmed in the AWX CLI reference.
- Removed: the legacy `AUTH_LDAP_TEAM_MAP`/`AUTH_LDAP_ORGANIZATION_MAP`/`SOCIAL_AUTH_SAML_TEAM_MAP`
  setting names, the `--team`/`--all` awx flag forms and the per-API-field role-name list
  (`admin_role`, `execute_role`, `use_role`) — kept only the documented `role_level=admin_role`
  filter example.
Method: documentation only; no commands were run.
