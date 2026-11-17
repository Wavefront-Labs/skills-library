---
id: computing-software.devops-ci-cd.verdaccio.team-access-and-unpublish
name: team-access-and-unpublish
category: computing-software
field: devops-ci-cd
product: verdaccio
tags: [team-access, unpublish, group-permissions, group-based-access, unpublish-permission, 403-forbidden]
level: practitioner
status: docs-checked
description: "Restrict packages to teams with group names in access and publish, split unpublish from publish, and what a user outside the group sees (403)."
sources:
  - https://verdaccio.org/docs/protect-your-dependencies/
  - https://verdaccio.org/docs/packages/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Protect a prefix for specific groups:

```yaml
'my-company-*':
  access: admin teamA teamB teamC
  publish: admin teamA
```
teamA and admin can publish; all four can read. A user in teamD gets `403 Forbidden` when installing a matching package, and the packages are hidden in the web UI for them. Use a naming prefix (or scope) so protection is easy to apply.

Recipes from the protection page:
- Default: `access: $all`, `publish: $authenticated`.
- Everything private: both `$authenticated`.
- Read-only mirror: `access: $all`, no `publish`, `proxy: npmjs`.

Unpublish is separate from publish:
```yaml
'jquery':
  access: $all
  publish: $all
  unpublish: root
'my-company-*':
  access: $all
  publish: $authenticated
  unpublish:          # empty: nobody may unpublish
'@my-local-scope/*':
  publish: $authenticated
  # unpublish omitted: falls back to publish
```
Groups come from the auth plugin; Verdaccio only checks membership. Restart after editing.

Verify: as a user outside the allowed groups, installing a matching package is refused with 403.

## Checked

2026-11-04. Read the Verdaccio documentation pages: Protecting packages and Package Access. Confirmed: the group-restricted config, the 403 for a user outside the groups, hidden packages in the web UI, the three recipes, the unpublish examples and the fallback to publish. Removed or corrected: the made-up package name and the npm whoami verify line.

Method: documentation only; no commands were run.
