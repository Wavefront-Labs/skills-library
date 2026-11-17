---
id: computing-software.cloud-infrastructure-engineering.azure.entra-administrative-units-and-directory-roles
name: entra-administrative-units-and-directory-roles
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, entra-id, administrative-units, directory-roles, entra-roles, scoped-roles, restricted-management-au, dynamic-administrative-units, role-assignable-groups, least-privilege, global-administrator, helpdesk-administrator, custom-entra-roles]
level: practitioner
status: gated
description: "Scope Entra directory roles with administrative units: build AUs (including restricted management), assign scoped roles and choose least-privilege built-in roles."
sources: ["https://learn.microsoft.com/entra/identity/role-based-access-control/administrative-units", "https://learn.microsoft.com/entra/identity/role-based-access-control/admin-units-restricted-management", "https://learn.microsoft.com/entra/identity/role-based-access-control/admin-units-assign-roles"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Administrative units and directory roles — delegate tenant admin without handing out Global Admin

**Goal:** regional/departmental helpdesks and app owners get exactly the directory role they
need, scoped to exactly their users, groups and devices.

## 1. Pick the role first (least privilege)
| Need | Role (not Global Admin) |
|---|---|
| Reset passwords for non-admins, invalidate tokens | Helpdesk Administrator / Password Administrator |
| Manage users and groups | User Administrator / Groups Administrator |
| Manage auth methods incl. MFA | Authentication Administrator (Privileged for admins) |
| Register/own apps | Application Developer / Cloud Application Administrator |
| Conditional Access | Conditional Access Administrator (+ Security Reader to view) |
| Read everything | Global Reader |
`az rest -m GET -u "https://graph.microsoft.com/v1.0/directoryRoleTemplates"` lists templates;
roles that can manage other admins (Privileged Role/Authentication Admin, Global Admin) are
**privileged** and should be PIM-eligible only.

## 2. Build administrative units
```bash
# static AU
az rest -m POST -u https://graph.microsoft.com/v1.0/directory/administrativeUnits \
  -b '{"displayName":"AU-EMEA","description":"EMEA helpdesk scope"}'
# add members
az rest -m POST -u https://graph.microsoft.com/v1.0/directory/administrativeUnits/<AU-ID>/members/\$ref \
  -b '{"@odata.id":"https://graph.microsoft.com/v1.0/users/<USER-ID>"}'
```
- Members can be users, groups and devices; see the administrative units page for what each object type supports.
- **Restricted management AU**: only administrators assigned a role at that AU scope can modify its members and properties; tenant-wide roles, including Global Administrator and Privileged Role Administrator, are blocked, though they can assign themselves at the AU. Use for executives, break-glass and admin accounts.

## 3. Assign scoped roles
```bash
az rest -m POST -u https://graph.microsoft.com/v1.0/roleManagement/directory/roleAssignments \
  -b '{"principalId":"<HELPDESK-GROUP-ID>","roleDefinitionId":"<ROLE-TEMPLATE-ID>","directoryScopeId":"/administrativeUnits/<AU-ID>"}'
```
(look up the role template id; `directoryScopeId: "/"` = tenant-wide.) The Graph request shapes above and the role names in section 1 come from pages not fetched in this review (gated: unconfirmed, source is paywalled or blocked).
Prefer assigning to a **role-assignable group** (`isAssignableToRole: true`, set at creation) over individuals.

## 4. Operate
- Only some roles can be scoped to an administrative unit; check the role table on the assign-roles page before designing.
- Review assignments at the AU scope through the Graph role assignments API and review privileged roles regularly with access reviews.

## Gotchas
- An AU adds scope for the AU-assigned admin; it does not stop a tenant-wide role from acting on its members (except restricted management AUs).
- Entra directory roles are not Azure RBAC: a Global Admin has no subscription access until elevating (see `rbac-elevate-access`).

## Verify
- [ ] An AU-scoped Helpdesk Admin can reset a password for an AU member but not for a user outside the AU.
- [ ] Restricted management AU: a tenant-wide User Admin cannot change an executive's phone number.

## Checked
2026-10-28. Confirmed on the administrative units, restricted management and assign-roles pages: AU-scoped role assignment, Authentication and Helpdesk Administrator roles at AU scope, restricted management AUs block Global Administrator and Privileged Role Administrator unless explicitly assigned at the AU, and those admins can assign themselves.
Gated: the Graph request shapes (graph.microsoft.com returns 401 to scripts) and the section 1 role list from the built-in roles reference, both marked in the text.
Removed (not confirmed): the 5 Global Admins target, dynamic AU example and P1 note, the one-restricted-AU and no-dynamic-membership claims, the role template GUID, the role-assignable group limit, the KQL alert query, and several operate/gotcha claims.

Method: documentation only; no commands were run.
