---
id: computing-software.data-science-and-analytics.bi-tools.pbi-row-level-security
name: pbi-row-level-security
category: computing-software
field: data-science-and-analytics
product: bi-tools
tags: [row-level-security, rls-roles, user-principal-name, pbi-governance]
level: practitioner
status: docs-checked
description: "Restrict rows by role with DAX filters, test with View as, and assign users to roles in the service."
sources:
  - https://learn.microsoft.com/power-bi/enterprise/service-admin-rls
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# RLS
Modeling tab > Manage roles > New: define a DAX filter on a table, for example
```dax
[Region] = "EU"
-- dynamic:
[UserEmail] = USERPRINCIPALNAME ()
```
In the service: semantic model > Security > add members to the role. Users with the workspace Contributor role or higher see the Security option; ownership or Build permission may also be needed. Test with "View as role" (also called Test as role).
## Gotchas
- RLS restricts only users with Viewer permissions; it does not apply to workspace Admin, Member or Contributor roles.
- By default RLS filters flow in a single direction, even across bi-directional relationships. "Apply security filter in both directions" on a relationship enables the other direction (for one relationship per table), but can hurt performance; test first.
- USERPRINCIPALNAME() returns the sign-in UPN, not necessarily the email address, and for B2B guests may return a #EXT# format; store in the mapping table exactly what the function returns and test with real guest users.
- Test as role uses your own identity, does not work for DirectQuery models with SSO enabled or for paginated reports, and cannot validate Q&A, Quick insights or Copilot.
- With an embedded app authenticating as a service principal, USERPRINCIPALNAME() and USERNAME() return the application ID or an empty string.
- Analysis Services live connections: RLS is configured in the model, not in Power BI.
## Verify
- [ ] "View as role" shows only the permitted rows, then check as a real Viewer-role user for dynamic RLS.

## Checked
Confirmed on the Power BI RLS page: Manage roles steps, Viewer-only scope, USERPRINCIPALNAME() dynamic example, Security page and who sees it, View/Test as role limitations, single-direction default and bi-directional option, B2B and service principal identity notes, live connection note. Removed: "RLS does not stop users with Build permission exporting underlying data in some scenarios", which the page does not state.
Method: docs-checked 2026-11-09 against the Microsoft Learn RLS page (now in the Fabric security section), selected sections read after grep.
