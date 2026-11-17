---
id: computing-software.cybersecurity-defensive.identity-access-management.administrative-units
name: administrative-units
category: computing-software
field: cybersecurity-defensive
product: identity-access-management
tags: [administrative-units, entra-administrative-units, role-scoping, restricted-management, delegated-administration, cloud-identity, least-privilege]
level: practitioner
status: docs-checked
description: "Scope Entra admin roles with administrative units: AU design, dynamic membership, restricted management AUs for sensitive accounts, and scoped role assignments via PIM."
sources: ["https://learn.microsoft.com/en-us/entra/identity/role-based-access-control/administrative-units", "https://learn.microsoft.com/en-us/entra/identity/role-based-access-control/admin-units-restricted-management", "https://learn.microsoft.com/en-us/entra/identity/role-based-access-control/admin-units-assign-roles"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Administrative units and role scoping

Tenant-wide roles (User Administrator, Helpdesk Administrator, Authentication Administrator) can reset
passwords/MFA for almost anyone. Administrative units (AUs) limit them to a subset.

## Design
- AUs by region, business unit or subsidiary, matching how support is delegated.
- **Dynamic membership** rules (`user.country -eq "DE"` or `user.department -eq "Sales"`) keep AUs current; check the licensing requirements.
- Assign roles scoped to the AU: Identity Governance -> Roles and admins -> AU -> Add assignment (or via PIM eligible assignments scoped to the AU).

## Restricted management AUs
For sensitive accounts (executives, break-glass, tier-0 admins, service accounts): create an AU with
"Restricted management administrative unit" = Yes.
Only admins assigned a role scoped to that AU can modify its members; tenant-scoped admins, including
Global Administrators, cannot (role assignments can still be changed by privileged role holders;
see the restricted management article). This stops a helpdesk-level compromise resetting an executive's MFA.
```
# Entra admin center > administrative units > New; Restricted management = Yes (Graph: isMemberManagementRestricted)
```

## Gotchas
- Roles that cannot be scoped to an AU still apply tenant-wide (see the AU role assignment article for which can).
- Privileged users are protected from lower-privilege admins by the role hierarchy, but other sensitive users are not - that is what restricted AUs fix.

## Verify
- [ ] Helpdesk role assignments scoped to AUs, not tenant-wide.
- [ ] Executive accounts in a restricted management AU; test that a tenant Helpdesk Admin cannot reset them.

## Checked

2026-10-28. Confirmed against the administrative units and restricted management pages: restricted management administrative units, IsMemberManagementRestricted in the audit log. Removed: dynamic membership P1 requirement, Privileged Role Administrator override detail, New-MgDirectoryAdministrativeUnit command, Helpdesk-versus-Global-Admin claim, device and group AU membership gotcha.

Method: documentation only; no commands were run.
