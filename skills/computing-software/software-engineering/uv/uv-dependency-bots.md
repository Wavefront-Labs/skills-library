---
id: computing-software.software-engineering.uv.uv-dependency-bots
name: uv-dependency-bots
category: computing-software
field: software-engineering
product: uv
tags: [uv, renovate, dependabot, dependency-updates, uv-lock, lockfile-maintenance, exclude-newer, cooldown]
level: practitioner
status: docs-checked
description: "Configure Renovate and Dependabot to update uv.lock, inline script metadata and cooldowns that match uv's exclude-newer setting."
sources: [https://docs.astral.sh/uv/guides/integration/renovate/, https://docs.astral.sh/uv/guides/integration/dependabot/]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Renovate and Dependabot with uv

Goal: automated dependency update PRs that keep `pyproject.toml` and `uv.lock` consistent.

## Method

### Renovate

A `uv.lock` file tells Renovate the project uses uv. It proposes upgrades to project, optional and development dependencies and updates both `pyproject.toml` and `uv.lock`.

Refresh the whole lockfile periodically (transitive dependencies) in `renovate.json5`:

```json5
{
  $schema: "https://docs.renovatebot.com/renovate-schema.json",
  lockFileMaintenance: {
    enabled: true,
  },
}
```

Inline script metadata (PEP 723) is supported, but Renovate cannot detect which Python files use it, so list them:

```json5
{
  pep723: {
    managerFilePatterns: ["docs/build.py", "scripts/**/*.py"],
  },
}
```

Renovate does not yet update the lock file attached to a script; update that by hand.

### Dependabot

Support is announced but some use cases do not work yet (tracked in astral-sh/uv issue 2512). Enable it by adding the uv ecosystem to `dependabot.yml`:

```yaml
version: 2

updates:
  - package-ecosystem: "uv"
    directory: "/"
    schedule:
      interval: "weekly"
```

### Cooldown alignment

If you set uv's `exclude-newer` (for example to `1 week`), set the bot's equivalent so it does not open PRs uv cannot lock.

Renovate:

```json5
{
  packageRules: [
    { matchDatasources: ["pypi"], minimumReleaseAge: "1 week" },
  ],
  // or for every ecosystem: minimumReleaseAge: "1 week",
}
```

Dependabot:

```yaml
    cooldown:
      default-days: 7
```

placed under the same `updates` entry.

## Gotchas

Without a matching cooldown, a bot may propose a version newer than `exclude-newer` allows, and the lock step fails.

## Checked

2026-11-07. Every command, flag, setting, default and example was read against the full text of the cited uv documentation pages (guides/integration/renovate; guides/integration/dependabot). Removed or changed: nothing needed removing.

Method: documentation only; no commands were run.
