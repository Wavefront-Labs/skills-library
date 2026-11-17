---
id: computing-software.devops-ci-cd.turborepo.ci-enable-remote-cache-turbo-token-and-team
name: ci-enable-remote-cache-turbo-token-and-team
category: computing-software
field: devops-ci-cd
product: turborepo
tags: [turborepo, ci, remote-cache, turbo-token, turbo-team, vercel-remote-cache, self-hosted-cache, ci-vendors]
level: practitioner
status: docs-checked
description: "Connect any CI to the Remote Cache with TURBO_TOKEN and TURBO_TEAM; Vercel CI is connected automatically."
sources:
  - https://raw.githubusercontent.com/vercel/turborepo/main/apps/docs/content/docs/crafting-your-repository/constructing-ci.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Turborepo speeds up builds, lints, tests and any other CI task through parallelisation and Remote Caching.

To enable Remote Caching in CI, set two environment variables so Turborepo can reach your Remote Cache:

- `TURBO_TOKEN`: the Bearer token used to access the Remote Cache.
- `TURBO_TEAM`: the account name associated with your repository. With the Vercel Remote Cache this is your team's slug.

When tasks run through `turbo`, CI can then hit the cache and speed up pipelines.

**Hosting notes from the docs**
- Vercel's built-in CI/CD is connected to your managed Vercel Remote Cache automatically with zero configuration.
- To connect other CI vendors to Vercel Remote Cache, get a token from the Vercel Remote Cache documentation ("use remote caching from external CI/CD").
- For self-hosted options, see Turborepo's Remote Cache API documentation.

Examples for specific vendors (GitHub Actions, GitLab CI, CircleCI, Buildkite, Travis CI, Vercel) live in the CI vendor guides.

## Checked

2026-11-04. Read in full from the vercel/turborepo docs source (apps/docs/content/docs/: crafting-your-repository/constructing-ci); commands, flags, key names, defaults and example values were matched against it. Removed: an unsourced advice sentence about treating the token as a secret and the Verify step.

Method: documentation only; no commands were run.
