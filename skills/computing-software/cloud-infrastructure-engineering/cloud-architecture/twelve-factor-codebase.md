---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.twelve-factor-codebase
name: twelve-factor-codebase
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, twelve-factor, 12-factor-app, twelve-factor-codebase, one-codebase-many-deploys, shared-libraries]
level: practitioner
status: docs-checked
description: "Apply factor I: one codebase per app in version control, many deploys from it; spot multi-codebase apps and apps that share code by copy instead of libraries."
sources: ["https://12factor.net/codebase"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Factor I: one codebase, many deploys

**Rule:** a twelve-factor app is always tracked in a version control system. A codebase is any single repo
(centralised systems such as Subversion) or any set of repos that share a root commit (decentralised systems
such as Git). There is always a one-to-one correlation between the codebase and the app.

## Audit
1. List apps and their repos.
   - If an app has multiple codebases, it is not an app but a distributed system. Each component of that system
     is an app and can comply with twelve-factor individually.
   - Multiple apps sharing the same code is a violation. Factor the shared code into libraries and include them
     through the dependency manager (factor II).
2. List the deploys of each app. A deploy is a running instance of the app: typically production plus one or more
   staging sites, and every developer's local copy also counts as a deploy.
3. Confirm all deploys come from the same codebase. Different versions may be active in each deploy (a
   developer has commits not yet on staging, staging has commits not yet in production), but they are still
   deploys of one app.

## Fix steps
- Several repos for one app: merge them into one codebase, or recognise the pieces as separate apps that talk
  to each other.
- Code copied between apps: extract it into a library with its own versioning and consume it through the
  dependency manager.

## Verify
- [ ] Every app maps to exactly one codebase.
- [ ] No two apps share source by copy; shared code arrives as a declared dependency.
- [ ] Each deploy can be traced to a commit in that one codebase (team practice, for example by recording the
  commit identifier at deploy time).

## Checked
2026-11-09. Confirmed against the 12factor.net Codebase page (read in full). Removed claims the page does not
make: monorepo tooling (Bazel, Nx, Turborepo), environment branches as an anti-pattern, feature flags, per-customer
fork advice and the git log check. The commit-identifier check is team practice, not a page claim.
Method: docs-checked 2026-11-09 against https://12factor.net/codebase (read in full); documentation only, no commands run.

Related: computing-software.cloud-infrastructure-engineering.cloud-architecture.build-release-run
