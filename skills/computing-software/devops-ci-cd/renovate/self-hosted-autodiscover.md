---
id: computing-software.devops-ci-cd.renovate.self-hosted-autodiscover
name: self-hosted-autodiscover
category: computing-software
field: devops-ci-cd
product: renovate
tags: [autodiscover, autodiscover-filter, repositories, renovate]
level: practitioner
status: docs-checked
description: "Run self-hosted Renovate across many repositories with autodiscover and autodiscoverFilter, or list repositories explicitly."
sources:
  - https://docs.renovatebot.com/self-hosted-configuration/#autodiscover
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

A self-hosted Renovate needs to know which repositories to process. Either list them in the global `repositories` array, or set `autodiscover` to `true`, in which case Renovate runs on every repository the bot account can access.

Narrow autodiscovery with `autodiscoverFilter`, an array of minimatch globs or RE2 regex strings matched against the `organization/repo` path. Multiple filters add up. When set through an environment variable or CLI, commas split filters, so commas inside a filter are not supported.

```json
{
  "platform": "github",
  "autodiscover": true,
  "autodiscoverFilter": ["my-org/*", "!my-org/old-*"]
}
```

Related options:

- `autodiscoverTopics` filters by repository topic.
- `autodiscoverNamespaces` and `autodiscoverProjects` filter by namespace or project on supported platforms.
- `autodiscoverRepoOrder` and `autodiscoverRepoSort` set the processing order.
- `writeDiscoveredRepos` makes Renovate write the discovered repositories to a JSON file and exit, for example `renovate --write-discovered-repos=/tmp/renovate-repos.json`; the docs name horizontal scaling setups as a use case.
- `includeMirrors`: by default mirror repositories are not autodiscovered; set `true` to include them.
- `ignorePrAuthor`: only for migrating the account Renovate runs as (or rotating GitLab project or group tokens). It makes Renovate fetch every PR in the repository, and on GitHub or GitLab every issue, instead of only its own.

Without a filter, `autodiscover` runs on every repository the Renovate account can access, so narrow it with `autodiscoverFilter` first.

## Checked

2026-11-08: read the `autodiscover`, `autodiscoverFilter`, `autodiscoverNamespaces`, `autodiscoverProjects`, `autodiscoverRepoOrder`, `autodiscoverRepoSort`, `autodiscoverTopics`, `writeDiscoveredRepos`, `includeMirrors`, `ignorePrAuthor` and `repositories` sections of the Self-Hosted Configuration page (raw source; partial read of that page). Confirmed autodiscover behaviour, filter syntax (minimatch or RE2, additive, comma limitation for env and CLI), and the descriptions of the related options. Removed the `requireConfig` and `onboarding` pairing advice and the onboarding-risk claim, which the sections do not state.
Method: documentation only; no commands were run.
