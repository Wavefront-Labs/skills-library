---
id: computing-software.cloud-infrastructure-engineering.ansible.controller-object-roles-and-resource-ownership
name: controller-object-roles-and-resource-ownership
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, controller-rbac, object-roles, grant-role, object-ownership, resource-ownership, awx-rbac]
level: practitioner
status: draft
description: "Grant object-level roles (admin, use, execute, read, update) on controller inventories, credentials, projects and templates to teams, and design organisation ownership."
sources: ["Red Hat AAP - Access management and authentication, roles (https://docs.redhat.com/en/documentation/red_hat_ansible_automation_platform/2.5/html/access_management_and_authentication/index)", "AWX documentation - Role-based access controls (https://ansible.readthedocs.io/projects/awx/en/latest/userguide/security.html#role-based-access-controls)", "ansible.controller / awx.awx role module (https://docs.ansible.com/ansible/latest/collections/awx/awx/role_module.html)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Controller object roles and resource ownership

## Ownership
Every inventory, project, credential, job template, workflow and notification template belongs
to **one organization**. Org admins administer everything in it; nothing is visible across orgs
unless explicitly granted. Design: one org per business unit/tenant, teams inside it.

## Object roles (what each allows)
| Object | Roles |
|---|---|
| Inventory | Admin, Update (sync sources), Ad Hoc (run ad hoc commands), Use (select in templates), Read |
| Credential | Admin, Use (attach to templates/inventory sources — secret never shown) |
| Project | Admin, Update (sync SCM), Use (select in templates), Read |
| Job template | Admin, Execute (launch), Read |
| Workflow template | Admin, Execute, Approve, Read |
| Organization | Admin, Auditor, Member, Read, Execute, Project/Inventory/Credential/Job Template/Workflow Admin, Notification Admin, Execution Environment Admin, Approval |

To **create** a job template a user needs Admin on the template (or org JT Admin) plus **Use** on
its inventory, project and credentials. To **launch**: Execute on the template only — the
operator never sees the credential.

## Granting as code
```yaml
- name: Ops team may run deploy templates
  awx.awx.role:                       # ansible.controller.role on AAP
    team: ops
    role: execute
    job_templates: [deploy-web, deploy-api]
    state: present

- name: Platform team uses the prod SSH credential
  awx.awx.role:
    team: platform
    role: use
    credentials: [prod-ssh]

- name: App devs read prod inventory
  awx.awx.role:
    team: app-devs
    role: read
    inventories: [prod]
```
In AAP 2.5+ with the platform gateway, role definitions (`ansible.platform.role_definition`,
`role_team_assignment`, `role_user_assignment`) are the newer API — check which your version exposes.

## Patterns
- Grant to **teams**, never individual users (users come and go via SSO team mapping).
- Separate "author" (Admin on JT, Use on inventory/project/credential) from "operator" (Execute).
- Credentials owned by a security/platform team; others get Use only.
- Auditors: org Auditor role for read-only across the org.

## Gotchas
- System Administrator / superuser bypasses everything — keep the list tiny, use SSO groups.
- Removing a user from a team does not remove roles granted to the user directly — audit direct grants (`/api/v2/users/<id>/roles/`).
- "Use" on an inventory lets users run any playbook from projects they can use against it — scope inventories carefully.

## Verify
- [ ] Log in as a test operator: can launch deploy-web, cannot view or edit prod-ssh, cannot edit the template.
- [ ] `/api/v2/teams/<id>/roles/` lists only the intended grants.
