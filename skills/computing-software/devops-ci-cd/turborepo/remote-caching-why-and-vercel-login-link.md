---
id: computing-software.devops-ci-cd.turborepo.remote-caching-why-and-vercel-login-link
name: remote-caching-why-and-vercel-login-link
category: computing-software
field: devops-ci-cd
product: turborepo
tags: [turborepo, remote-cache, turbo-login, turbo-link, vercel-remote-cache, sso-team, local-cache, verify-remote-cache]
level: practitioner
status: docs-checked
description: "Why local-only caching duplicates work in CI, how to enable the Vercel Remote Cache with turbo login and link, and how to verify it replays from remote."
sources:
  - https://raw.githubusercontent.com/vercel/turborepo/main/apps/docs/content/docs/core-concepts/remote-caching.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Turborepo's task cache saves time but is **local to your machine** by default. In CI, each machine re-executes `turbo run build` even when inputs are identical, wasting time. A Remote Cache is a server storing task results so teammates, CI and your PaaS share them. You do not need Remote Caching to use Turborepo, but it brings the most significant speedups. It is free, and can use a managed provider or be self-hosted.

**Vercel Remote Cache** is free on all plans, even if you do not host on Vercel. Steps:
1. `turbo login` (or `npx turbo login`, `pnpm dlx turbo login`, `yarn dlx turbo login`, `bunx turbo login`) authenticates the CLI with your Vercel account. With single sign-on use `turbo login --sso-team=team-name` to get a cache token with the right privileges.
2. `turbo link` links the repo to the Remote Cache.
3. Run tasks; artifacts are stored locally and remotely.

**Verify:** delete the local cache (`rm -rf ./.turbo/cache`, or `rd /s /q "./.turbo/cache"` on Windows) and run the same build. A working setup does not execute locally; `turbo` downloads logs and artifacts from the Remote Cache and replays them.

If you build and host on Vercel, Remote Caching is set up automatically once you use `turbo`.

Cautions from the docs: make sure caching is correct first, double check environment variable handling, and remember Turborepo treats **logs as artifacts**, so be aware of what you print to the console.

## Checked

2026-11-04. Read the Remote Caching page's introduction and Vercel sections in full: local-only default, free on all plans, login variants, `--sso-team`, `turbo link`, the verify-by-deleting-cache step and the Vercel auto-setup note match. The page's own verification step is kept.

Method: documentation only; no commands were run.
