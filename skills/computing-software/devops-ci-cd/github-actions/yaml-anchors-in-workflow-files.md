---
id: computing-software.devops-ci-cd.github-actions.yaml-anchors-in-workflow-files
name: yaml-anchors-in-workflow-files
category: computing-software
field: devops-ci-cd
product: github-actions
tags: [github-actions, yaml-anchors-workflows, yaml-aliases, workflow-syntax]
level: practitioner
status: verified
description: "Use YAML anchors (&name) and aliases (*name) in GitHub Actions workflows to dedupe steps/env, the merge-key limitation, and when a composite action is better."
sources: ["https://docs.github.com/en/actions/reference/workflows-and-actions/reusing-workflow-configurations#yaml-anchors-and-aliases", "https://github.blog/changelog/2025-09-18-actions-yaml-anchors-and-non-public-workflow-templates/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# YAML anchors and aliases in workflow files

GitHub Actions accepts YAML anchors/aliases in workflow files (announced in the GitHub changelog on
2025-09-18). Before that, anchors were not supported.

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    env: &common-env
      NODE_ENV: test
      TZ: UTC
    steps:
      - &checkout
        uses: actions/checkout@<sha>
        with: { fetch-depth: 0 }
      - run: npm test
  lint:
    runs-on: ubuntu-latest
    env: *common-env
    steps:
      - *checkout
      - run: npm run lint
```

## Gotchas
- **Merge keys**: GitHub's docs only show aliasing a whole node (`env: *common-env`,
  `alt-test: *base_job`). Merge keys (`<<: *base`) are not shown in the docs, so do not rely on them. Need
  "same but one key different"? Use a composite action, a reusable workflow, or workflow-level `env`.
- Anchors are file-scoped (a YAML property): they cannot cross into another workflow file.
- Define the anchor before any alias (YAML order). actionlint reports an alias to an undefined anchor
  (`unknown anchor 'base' referenced`) as a YAML parse failure for the whole file.
- Check whether your tooling copes: actionlint added anchor and alias support in 1.7.10 (and flags unused
  anchors); older versions, act and editor schemas may flag them. Upgrade before adopting.
- Readability: anchors hide where values come from. Keep them for genuinely identical blocks
  (checkout settings, env maps, service definitions), not as a templating system.

## When not to use
| Need | Better tool |
|---|---|
| Same steps across repos | composite action |
| Same job graph across repos | reusable workflow (`workflow_call`) |
| Same env for every job | top-level `env:` |

## Verify
- [ ] `actionlint` passes on the file.
- [ ] The run's "Set up job" step shows the expanded steps for both jobs.
