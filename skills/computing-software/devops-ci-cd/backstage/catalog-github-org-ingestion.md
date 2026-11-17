---
id: computing-software.devops-ci-cd.backstage.catalog-github-org-ingestion
name: catalog-github-org-ingestion
category: computing-software
field: devops-ci-cd
product: backstage
tags: [github-org, org-data, users-and-teams, backstage]
level: practitioner
status: docs-checked
description: "Import GitHub users and teams as User and Group entities with the githubOrg catalog provider."
sources:
  - https://backstage.io/docs/integrations/github/org
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

The GitHub org module ingests users and teams from a GitHub organisation, producing a hierarchy of `User` and `Group` entities that mirrors your setup.

```bash
yarn --cwd packages/backend add @backstage/plugin-catalog-backend-module-github-org
```

```ts
backend.add(import('@backstage/plugin-catalog-backend'));
backend.add(import('@backstage/plugin-catalog-backend-module-github-org'));
```

```yaml
catalog:
  providers:
    githubOrg:
      id: production
      githubUrl: https://github.com
      orgs: ['organization-1', 'organization-2']
      schedule:
        initialDelay: { seconds: 30 }
        frequency: { hours: 1 }
        timeout: { minutes: 50 }
```

- `orgs` lists the organisations to read, and `githubUrl` points to github.com or a GitHub Enterprise host.
- You can define several providers by using a list, each with its own `id` and `githubUrl`.
- `pageSizes` (`teams`, `teamMembers`, `organizationMembers`) tune GraphQL paging for large orgs.
- The schedule controls how often the whole org is re-read.

Before installing the provider, confirm the token or GitHub App permissions listed in the GitHub Locations and GitHub Apps docs. Sign-in resolvers need a matching User entity in the catalog, so import users before relying on GitHub sign-in.

## Checked

2026-11-03. Confirmed on the GitHub Org Data page: the module package, the `catalog.providers.githubOrg` block with `id`, `githubUrl`, `orgs` and `schedule` including `initialDelay`, a list form with several providers (for example a GitHub Enterprise host), `pageSizes` (`teams`, `teamMembers`, `organizationMembers`) and the permissions prerequisites. On the sign-in identity resolver page: sign-in fails without a matching User entity. Removed: the `integrations.github` and API rate limit remarks, which the page does not state.

Method: documentation only; no commands were run.
