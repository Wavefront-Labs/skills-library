---
id: computing-software.software-engineering.refactoring.major-framework-and-language-upgrades
name: major-framework-and-language-upgrades
category: computing-software
field: software-engineering
product: refactoring
tags: [refactoring, framework-upgrade, language-upgrade, dependency-upgrades, codemods, openrewrite]
level: advanced
status: draft
description: "Plan and execute major framework and language version upgrades: inventory, deprecation cleanup first, migration tools, incremental rollout, both versions building."
sources: ["https://docs.openrewrite.org/", "https://docs.djangoproject.com/en/stable/howto/upgrade-version/", "https://github.com/asottile/pyupgrade", "https://learn.microsoft.com/en-us/dotnet/core/porting/upgrade-assistant-overview"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Major framework and language version upgrades

## 1. Inventory and plan
- Current and target versions, end-of-support dates (endoflife.date), breaking-change lists /
  migration guides for each major version in between.
- Dependency graph: which libraries support the target? Blockers (an abandoned plugin) are found now.
- Test coverage of critical paths; add characterisation tests where thin.

## 2. Get warnings-clean on the current version
Most frameworks deprecate before removing. Run with deprecation warnings as errors
(`python -W error::DeprecationWarning`, `-Xlint:deprecation`, `TreatWarningsAsErrors` for obsolete
APIs, Django `python -Wa manage.py test`, React StrictMode). Fix them on the **old** version, ship.

## 3. Upgrade one step at a time
One major version at a time (Django LTS to LTS through each feature release's deprecations; Angular
`ng update` per major). Upgrade dependencies to versions that support both old and new where possible.

## 4. Automate the mechanical changes
| Ecosystem | Tool |
|---|---|
| Java/Spring Boot | OpenRewrite recipes (`UpgradeSpringBoot_3_0`, `Java17` migration), `jdeprscan` |
| Python | pyupgrade `--py312-plus`, django-upgrade, `ruff --select UP`, LibCST codemods |
| .NET | .NET Upgrade Assistant, `try-convert`, Roslyn analyzers |
| JS/TS | `ng update`, `npx @next/codemod`, React codemods, jscodeshift |
| Go | `go fix`, `gopls` modernize analyzers |
| Rust | `cargo fix --edition` |
Review the diff; tools miss semantic changes (behavioural defaults, removed implicit conversions).

## 5. Roll out safely
- Keep the build green on trunk: compatibility shims, or build both versions in CI matrix during
  transition (`tox` envs, multi-target `<TargetFrameworks>`).
- For services: canary the upgraded build, compare error rates and latency, roll forward.
- For monorepos: upgrade leaf packages first, or use per-package versions temporarily.

## 6. Finish
Remove shims and the old CI matrix entry, update docs and base images, record the next EOL date.
Schedule upgrades regularly; skipping several majors is what makes them projects.
