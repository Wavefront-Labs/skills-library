---
id: computing-software.devops-ci-cd.build-systems.renovate-custom-regex-managers
name: renovate-custom-regex-managers
category: computing-software
field: devops-ci-cd
product: build-systems
tags: [build-systems, renovate-custom-manager, regex-manager, renovate]
level: advanced
status: docs-checked
description: "Teach Renovate to update versions it cannot parse natively (Dockerfile ARGs, CI YAML env values) with customManagers regex definitions and datasource annotations."
sources: ["https://github.com/renovatebot/renovate/blob/main/lib/modules/manager/custom/regex/readme.md", "https://docs.renovatebot.com/configuration-options/#custommanagers", "https://docs.renovatebot.com/troubleshooting/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Renovate custom regex managers

Versions in `ARG TERRAFORM_VERSION=1.9.5` or in CI workflow `env:` blocks are invisible to built-in
managers. `customManagers` with `customType: regex` fix that.

## Annotation convention
Put a comment above the version telling Renovate the datasource and package:
```dockerfile
# renovate: datasource=github-releases depName=hashicorp/terraform
ARG TERRAFORM_VERSION=1.9.5
```
```yaml
# .github/workflows/ci.yml
env:
  # renovate: datasource=npm depName=pnpm
  PNPM_VERSION: 9.12.0
```

## Config (renovate.json)
```json
{
  "customManagers": [
    {
      "customType": "regex",
      "description": "Versions annotated with # renovate comments",
      "managerFilePatterns": ["/(^|/)Dockerfile$/", "/\\.ya?ml$/"],
      "matchStrings": [
        "# renovate: datasource=(?<datasource>[a-z-]+?) depName=(?<depName>[^\\s]+?)(?: versioning=(?<versioning>\\S+?))?\\s+(?:ARG\\s+|ENV\\s+)?\\S+?(?::|:?=)\\s*\"?(?<currentValue>[^\\s\"]+)\"?"
      ],
      "versioningTemplate": "{{#if versioning}}{{{versioning}}}{{else}}semver{{/if}}"
    }
  ]
}
```
`managerFilePatterns` is the current name of the option formerly called `fileMatch`; existing `fileMatch` config is migrated automatically. Patterns written as `/regex/` are regular expressions, other values are globs.

Required: `matchStrings` plus a `currentValue` (or `currentDigest`) capture group, a `depName` or `packageName` (group or `depNameTemplate`/`packageNameTemplate`) and a `datasource` (group or `datasourceTemplate`). Optional: `versioning` (group or `versioningTemplate`; Renovate's default is `semver-coerced`), `extractVersion` (group or `extractVersionTemplate`, for example to strip a leading `v`) and `registryUrl` (group or `registryUrlTemplate`).

## Debug
```bash
LOG_LEVEL=debug npx renovate --platform=local
```
The `local` platform performs a dry run against the current directory (default `dryRun=lookup`; `--dry-run=extract` stops after extraction). Look in the debug log for the dependencies your custom manager extracted.

## Verify
- [ ] Renovate dependency dashboard lists the annotated dependencies; a PR bumps the ARG value.

## Checked
Date: 2026-10-25. Documentation: Renovate `lib/modules/manager/custom/regex/readme.md`, `docs/usage/configuration-options.md`, `docs/usage/troubleshooting.md` and `lib/modules/platform/local/readme.md` (renovatebot/renovate, main branch).
Confirmed: `customType: regex`, `managerFilePatterns` (formerly `fileMatch`, auto-migrated), `matchStrings`, required and optional capture groups and their template equivalents, default versioning `semver-coerced`, the `# renovate: datasource=... depName=...` annotation convention, `LOG_LEVEL=debug`, `--platform=local` and its `lookup`/`extract` dry-run behaviour.
Fixed: the example `matchStrings` expression could not match a Dockerfile `ARG NAME=value` line (it required the name to follow the annotation directly); it now accepts an optional `ARG`/`ENV` keyword and `=`, `:` or `:=`. The Makefile file pattern was removed because the expression is not designed for it.
Removed: the `--dry-run=lookup` combination with a "packageFiles with updates" log message (not in the documentation).
Method: documentation only; no commands were run.
