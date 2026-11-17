---
id: computing-software.cloud-infrastructure-engineering.harbor.project-roles-and-permissions
name: project-roles-and-permissions
category: computing-software
field: cloud-infrastructure-engineering
product: harbor
tags: [project-roles, limited-guest, project-admin, rbac, harbor]
level: practitioner
status: docs-checked
description: "Pick the right Harbor project role from Limited Guest to ProjectAdmin, and know which actions only the system administrator can perform."
sources:
  - https://goharbor.io/docs/main/administration/managing-users/user-permissions-by-role/
  - https://goharbor.io/docs/main/administration/managing-users/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Harbor grants access through project membership with one of five roles, plus two system roles.

- **Limited Guest**: can pull images and see repositories, images, vulnerabilities and project configuration, but cannot see logs or the member list. Intended for users from other organizations.
- **Guest**: read-only. Can pull and retag images (retag needs push permission on the destination), and see logs and members.
- **Developer**: read and write. Can push, create repositories, add or remove image labels, upload helm charts, create, read and export project vulnerability lists, and create, delete, enable or deactivate tag retention rules.
- **Maintainer**: adds scan and delete image, edit and delete repositories, manage labels, view replications and webhook events, see project robots, and manage tag immutability rules.
- **ProjectAdmin**: the role assigned to whoever creates a project. Adds edit of project configuration, member management, project robots, CVE allowlist, webhooks, scanner selection, replication jobs view and project deletion.
- **Harbor system administrator**: all permissions, plus listing all projects, making users administrators, deleting users and setting the vulnerability scan policy for all images. Only the system administrator can add scanners and edit project quotas.
- **Anonymous**: no access to private projects and read-only on public projects.

On public projects every user can list repositories, images and vulnerabilities, pull and retag images, and download helm charts.

In LDAP/AD or OIDC mode users are created in the external provider; Harbor shows them in the Users tab. Deleting a user in those modes removes only the Harbor data, not the provider account. Select users and click **Set as Administrator** to grant the system administrator role.

## Checked

2026-11-03. Each role's permissions were read against the table on the Harbor docs page User Permissions By Role; the role descriptions, the two system roles, public-project access and LDAP/OIDC user handling against Managing Users. Corrected: Developer vulnerability permissions (the table lists create, read and export of project vulnerability lists; scanning is Maintainer and above), the system administrator's global policy, and the ProjectAdmin wording.

Method: documentation only; no commands were run.
