---
id: computing-software.devops-ci-cd.build-systems.renovate-configuration-and-presets
name: renovate-configuration-and-presets
category: computing-software
field: devops-ci-cd
product: build-systems
tags: [build-systems, dependency-pinning, renovate, renovate-config, renovate-presets, renovate-json, packagerules, shareable-config, dependency-dashboard, pin-digests, schedule, minimumreleaseage, custom-managers, self-hosted-renovate]
level: practitioner
status: draft
description: "Configure Renovate well: renovate.json basics, org shareable presets, packageRules grouping, schedules and PR limits, digest pinning, minimumReleaseAge and regex custom managers."
sources: ["https://docs.renovatebot.com/configuration-options/", "https://docs.renovatebot.com/config-presets/", "https://docs.renovatebot.com/presets-config/", "https://docs.renovatebot.com/modules/manager/regex/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Renovate configuration and presets

## Minimal repo config
```json5
// renovate.json5 (or renovate.json / .github/renovate.json5)
{
  $schema: "https://docs.renovatebot.com/renovate-schema.json",
  extends: ["github>acme/renovate-config"],     // org preset; everything else lives there
}
```

## Org shareable preset (repo acme/renovate-config, file default.json)
```json5
{
  extends: [
    "config:recommended",            // sensible defaults, dependency dashboard, monorepo groups
    ":semanticCommits",
    "helpers:pinGitHubActionDigests", // actions pinned to SHA with version comment
    "docker:pinDigests",             // FROM image:tag@sha256:...
    ":pinDevDependencies",
  ],
  timezone: "Europe/London",
  schedule: ["before 6am on monday"],
  prConcurrentLimit: 10,
  prHourlyLimit: 4,
  minimumReleaseAge: "3 days",       // wait for new releases to settle (and for yanks)
  internalChecksFilter: "strict",    // don't open PRs until the age check passes
  labels: ["dependencies"],
  packageRules: [
    { matchUpdateTypes: ["major"], dependencyDashboardApproval: true },
    { matchManagers: ["github-actions"], groupName: "github actions", schedule: ["before 6am on the first day of the month"] },
    { matchPackageNames: ["/^@aws-sdk//"], groupName: "aws sdk" },
    { matchDepTypes: ["devDependencies"], matchUpdateTypes: ["minor", "patch"], groupName: "dev deps (non-major)" },
    { matchDatasources: ["docker"], matchPackageNames: ["postgres"], allowedVersions: "<17" },
  ],
  vulnerabilityAlerts: { labels: ["security"], schedule: ["at any time"] },
}
```
- Presets can live at `github>org/repo`, `github>org/repo:preset-file`, `gitlab>...`,
  `local>org/repo` (same platform as the bot). Versioned via `#v1.2.0` suffix.
- `packageRules` apply in order; later matches override earlier ones.
- `matchPackageNames` accepts exact names, globs and `/regex/` (older
  `matchPackagePatterns` is deprecated).

## Pinning philosophy
- Apps: pin exact versions (`rangeStrategy: "pin"` or lockfiles), Docker digests, Action
  SHAs. Libraries: keep ranges (`rangeStrategy: "bump"` or `"widen"`), lockfile
  maintenance (`lockFileMaintenance: { enabled: true, schedule: [...] }`).

## Custom managers (versions in arbitrary files)
```json5
customManagers: [{
  customType: "regex",
  managerFilePatterns: ["/(^|/)Dockerfile$/", "/\\.ya?ml$/"],   // fileMatch on older versions
  matchStrings: ["# renovate: datasource=(?<datasource>\\S+) depName=(?<depName>\\S+)\\s+\\S+[:=]\\s*\"?(?<currentValue>[^\"\\s]+)"],
}]
```
Then annotate: `# renovate: datasource=github-releases depName=helm/helm` above
`HELM_VERSION=3.16.1`.

## Operate
- **Dependency Dashboard** issue: approve majors, retry, see rate-limited/pending PRs.
- Validate config: `npx --package renovate renovate-config-validator` in CI on the preset repo.
- Debug a repo: run locally `LOG_LEVEL=debug npx renovate --platform=local` or read the
  Mend app job logs.

## Verify
Config validator passes; onboarding PR (or dashboard) lists the expected groups; a new
Docker base image release produces a PR only after `minimumReleaseAge`.
