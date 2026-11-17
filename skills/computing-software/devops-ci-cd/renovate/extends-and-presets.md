---
id: computing-software.devops-ci-cd.renovate.extends-and-presets
name: extends-and-presets
category: computing-software
field: devops-ci-cd
product: renovate
tags: [extends, presets, config-recommended, renovate]
level: practitioner
status: docs-checked
description: "Use the extends array to inherit config presets such as config:recommended and group, schedule and default helper presets."
sources:
  - https://docs.renovatebot.com/key-concepts/presets/
  - https://docs.renovatebot.com/config-presets/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

A preset is a reusable chunk of Renovate configuration stored in JSON, JSON5 or JSONC. You apply presets through the `extends` array. Presets are modular and can themselves extend other presets. Presets that ship with Renovate are referenced by name; custom presets are referenced by repository location (see the Shareable Config Presets page).

```json
{
  "extends": ["config:recommended", "helpers:pinGitHubActionDigests"]
}
```

Rules to remember:

- If two presets conflict logically, the last entry in `extends` wins.
- `config:recommended` is Renovate's default configuration and the onboarding PR suggests it. It mostly uses defaults plus smart customizations such as grouping monorepo packages. Self-hosters must set `onboardingConfig` to get it in onboarding PRs.
- The `:xyz` prefix is shorthand for `default:xyz`, for example `:dependencyDashboard`.
- Browse the `schedule:` presets for options such as `schedule:nonOfficeHours`.
- Presets can take parameters, one per `{{argN}}` in the definition: `":labels(dependencies,devops)"` and `":assignee(renovate-tests)"`.
- `ignorePresets` entries are matched against the resolved preset string, not a relative reference written inside a preset (see the Shareable Config Presets page for the relative-form cases).
- Describe a custom preset with a `description` field, or use comments in JSONC.
- To manage many repositories, create one global preset and extend it from each repository.

## Checked

2026-11-08: read the whole Presets key-concepts page and the whole Shareable Config Presets page (raw sources of docs.renovatebot.com/key-concepts/presets and config-presets). Confirmed `extends` usage, last-preset-wins, `config:recommended` as the default and onboarding suggestion, `:xyz` meaning `default:xyz`, `schedule:nonOfficeHours`, parameter syntax, `ignorePresets` matching resolved strings, and global presets for many repositories. Removed `group:monorepos`, `schedule:weekly`, `config:best-practices`, `:disableHost(...)`, the `:app` and `:library` claims and the "thin config" advice, which the pages do not state.
Method: documentation only; no commands were run.
