---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.build-release-run
name: build-release-run
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, twelve-factor, 12-factor-app, build-release-run, release-id, rollback, immutable-releases]
level: practitioner
status: docs-checked
description: "Apply factor V: separate build, release (build plus config, unique immutable id) and run stages so releases are reproducible and rollback means picking an old release."
sources: ["https://12factor.net/build-release-run"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Factor V: strictly separate build, release and run

- **Build stage**: converts a code repo at a commit specified by the deployment process into an executable
  bundle (a build). It fetches vendored dependencies and compiles binaries and assets.
- **Release stage**: combines the build with the deploy's current config. The resulting release contains both
  and is ready for immediate execution.
- **Run stage** (runtime): launches a set of the app's processes against a selected release.

The twelve-factor app uses strict separation of the three. For example, it is impossible to change code at
runtime, because there is no way to propagate such a change back to the build stage.

## Steps
1. Give every release a unique ID, such as a timestamp (2011-04-06-20:32:17) or an incrementing number (v100).
2. Treat releases as an append-only ledger. A release cannot be mutated once created; any change, config
   included, creates a new release.
3. Use deployment tooling that offers release management and rollback. The page cites Capistrano, which stores
   releases in a `releases` subdirectory, points the current release at one by symlink, and has a `rollback`
   command to return to a previous release.
4. Keep the run stage to as few moving parts as possible. It can start automatically (a server reboot, or a
   process manager restarting a crashed process) when no developer is around. The build stage can be more
   complex because its errors are always in front of the developer driving the deploy.

## Gotchas
- Editing files on a running host breaks the separation: the change cannot flow back into a build.
- A config change without a new release ID leaves "what is running" unanswerable.

## Verify
- [ ] Every running deploy reports a release ID that maps to one build and one config.
- [ ] Rolling back means selecting a previous release, not rebuilding.

## Checked
2026-11-09. Confirmed against the 12factor.net Build, release, run page (read in full). Removed claims the page
does not make: image digests, mutable tag warnings, per-platform release mechanisms (Helm, Argo CD, ECS, Cloud
Run, Lambda, App Service), the specific rollback commands, the release ledger fields and database
expand/contract advice.
Method: docs-checked 2026-11-09 against https://12factor.net/build-release-run (read in full); documentation only, no commands run.
