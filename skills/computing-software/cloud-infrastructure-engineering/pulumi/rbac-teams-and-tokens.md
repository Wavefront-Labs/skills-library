---
id: computing-software.cloud-infrastructure-engineering.pulumi.rbac-teams-and-tokens
name: rbac-teams-and-tokens
category: computing-software
field: cloud-infrastructure-engineering
product: pulumi
tags: [cloud-infrastructure-engineering, pulumi, access-tokens, pulumi-teams, org-token, rbac]
level: practitioner
status: docs-checked
description: "Control Pulumi Cloud access with built-in and custom roles, teams, creator grants and personal, team and organization access tokens for CI."
sources:
  - https://www.pulumi.com/docs/administration/concepts/rbac/
  - https://www.pulumi.com/docs/administration/concepts/access-tokens/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# RBAC, teams and access tokens

**Roles.** Built-in roles are Reader, Builder, Maintainer, Admin and Billing Manager, available in all editions including Essentials. Custom roles, custom permission sets, teams and tag-based (ABAC) rules need Pro or Enterprise. Building blocks: scopes, bundled into permission sets, applied to entities (stacks, environments, cloud accounts) to form entity access rules; a role combines rules with an organization access level. Each member has exactly one organization role (the org default unless changed). A user's effective permissions are the union of their role, their teams' roles and direct entity grants, and creator grants; all grants are additive, so nothing can revoke access another rule gives.

**Token types.**
- Personal: carries your user's permissions across all your organizations; every user can create them.
- Organization (Essentials, Pro, Enterprise): authenticates as the organization, appears in audit logs as the organization; recommended for CI/CD, drift detection and policy automation. Assign a custom role holding only the scopes the automation needs.
- Team (Pro, Enterprise): authenticates as a team; its permissions are the union of the team's roles, evaluated per request.

Practice:
- Give every token an expiry (up to two years); admins can enforce a maximum with an access token expiry policy. Expired tokens cannot be reactivated.
- Org and team tokens are machine tokens: use them for pipelines, not for people.
- Token names must be unique across org and team tokens, including deleted ones.
- Creating or deleting an organization token needs a user credential such as a personal token; a machine token gets `403 Forbidden: Machine tokens are not allowed to perform this operation`. Use a personal token of a dedicated service-account user to automate that.
- Org admins manage org tokens under Settings > Access Management > Access Tokens; org and team admins manage team tokens under Teams > (team) > Access Tokens.

## Gotchas
- A stack created with a token gives that machine identity a permanent Stack Admin creator grant. Transfer ownership to a break-glass user or team (stack Access > Settings > Change owner), or delete the entry on the stack's Access tab.
- Tokens without a role use the org-wide settings (stack permissions None/Read/Write, where Write excludes deleting stacks; environment and account permissions; create stacks/accounts/teams toggles); change them under Settings > Access management > Access Tokens tab.
- Deleting a token revokes it immediately.

## Checked
2026-11-03. Confirmed on the Pulumi Cloud RBAC and access tokens pages. Removed: `PULUMI_ACCESS_TOKEN`, `pulumi whoami/org set-default` commands, the unconfirmed REST PATCH team path, OIDC token exchange claim, "stack not found" explanation and the old Admin/Member three-role list.
Method: documentation only; no commands were run.
