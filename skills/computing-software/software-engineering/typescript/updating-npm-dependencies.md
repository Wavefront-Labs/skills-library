---
id: computing-software.software-engineering.typescript.updating-npm-dependencies
name: updating-npm-dependencies
category: computing-software
field: software-engineering
product: typescript
tags: [typescript, npm-outdated, npm-dedupe, npm-update, renovate, npm-check-updates, npm]
level: practitioner
status: verified
description: "Keep npm dependencies current safely: npm outdated and update semantics, major upgrades with ncu, dedupe, why/ls to trace versions, and Renovate/Dependabot grouping and automerge."
sources: ["https://docs.npmjs.com/cli/v10/commands/npm-outdated", "https://docs.npmjs.com/cli/v10/commands/npm-update", "https://docs.npmjs.com/cli/v10/commands/npm-dedupe", "https://docs.renovatebot.com/configuration-options/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Updating npm dependencies

**Goal:** small, frequent, reviewable dependency updates instead of a yearly
big-bang upgrade.

## See what's stale
```bash
npm outdated              # Current / Wanted (max satisfying your range) / Latest
npm outdated --long --all
```
"Wanted" < "Latest" means the new version is outside your semver range (usually a major).

## Within ranges
```bash
npm update                # updates lockfile to Wanted for direct + transitive deps
npm update lodash         # just one
npm install react@^19     # move a range (edits package.json)
```
`npm update` kept the `^7.0.0` range in `package.json` and moved only the lockfile (7.0.0 to 7.8.5 in a test on npm 10.8).

## Majors
```bash
npx npm-check-updates -i            # interactive: pick upgrades, rewrites package.json ranges
npx npm-check-updates --target minor -u
```
One major at a time, read the changelog/migration guide, run tests, commit per package.

## Tracing versions
```bash
npm ls react --all          # where each copy comes from
npm explain semver          # (= npm why) dependency chain for a package
npm dedupe                  # hoist/merge compatible duplicates in the lockfile
npm query ':outdated(major)' # selector-based querying (ran on npm 10.8; returns JSON)
```
Multiple copies of singletons (react, graphql, @types/react) cause "Invalid hook call" or
instanceof failures - dedupe, align ranges, or use `overrides`.

## Automate with Renovate (or Dependabot)
```json
{
  "extends": ["config:recommended", ":semanticCommits"],
  "schedule": ["before 6am on monday"],
  "packageRules": [
    { "matchUpdateTypes": ["minor", "patch"], "matchCurrentVersion": "!/^0/", "groupName": "non-major", "automerge": true },
    { "matchPackageNames": ["/^@types\\//"], "groupName": "types", "automerge": true },
    { "matchUpdateTypes": ["major"], "dependencyDashboardApproval": true }
  ],
  "minimumReleaseAge": "3 days",
  "lockFileMaintenance": { "enabled": true }
}
```
- `minimumReleaseAge` delays brand-new versions (compromised releases are usually yanked fast). This config passes `renovate-config-validator`.
- Automerge requires good CI; group noisy packages; majors behind approval.
- `lockFileMaintenance` refreshes transitive deps weekly.

## After updating
`npm ci && npm test && npm run build`, check bundle size changes, `npm audit` diff.

## Verify
- [ ] `npm outdated` shows no patch/minor drift older than a month.
- [ ] Each update PR is green on full CI before merge; majors have a linked changelog.
