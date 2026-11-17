---
id: creative-arts.design-for-form-and-experience.design-systems.building-a-token-sync-pipeline
name: building-a-token-sync-pipeline
category: creative-arts
field: design-for-form-and-experience
product: design-systems
tags: [token-pipeline, tokens-studio, design-token-sync, figma-variables-sync, style-dictionary, token-automation, github-actions]
level: practitioner
status: draft
description: "Build a design token pipeline: source of truth in Figma variables or Tokens Studio, sync to Git via PR, transform with Style Dictionary, publish packages and test."
sources:
  - "Tokens Studio for Figma documentation (docs.tokens.studio)"
  - "Style Dictionary (styledictionary.com)"
  - "Design Tokens Community Group format (design-tokens.github.io/community-group/format)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Token sync pipeline

**Goal:** a change to a colour or spacing token in design reaches every platform automatically, reviewed and versioned.

## Choose the source of truth
- **Figma variables** (native; use REST API or a plugin to export) or **Tokens Studio** (JSON in Git with multi-file sets, themes and aliases) or **code-first** JSON edited by engineers with a Figma import. Pick one; two-way sync causes conflicts.

## Pipeline
1. **Author:** designers edit variables or Tokens Studio sets; naming per convention (`color.bg.surface`, tier primitive to semantic to component; see `creative-arts.design-for-form-and-experience.design-systems.design-tokens-and-a-modular-type-scale`).
2. **Sync to Git:** Tokens Studio "Sync to GitHub/GitLab" pushes JSON to a branch and opens a PR; with Figma variables run an export action using the Variables REST API (`GET /v1/files/:key/variables/local`, Enterprise plan) or a plugin such as Variables to JSON, committing DTCG-format files.
3. **Validate in CI:** JSON schema or DTCG lint, alias resolution (no dangling references), contrast matrix for pairs, naming rules.
4. **Transform:** Style Dictionary v4 with custom formats/transforms:
```js
export default { source: ['tokens/**/*.json'], platforms: {
  css: { transformGroup: 'css', buildPath: 'dist/css/', files: [{ destination: 'tokens.css', format: 'css/variables' }] },
  ios: { transformGroup: 'ios-swift', buildPath: 'dist/ios/', files: [{ destination: 'Tokens.swift', format: 'ios-swift/class.swift' }] },
  android: { transformGroup: 'android', buildPath: 'dist/android/', files: [{ destination: 'tokens.xml', format: 'android/resources' }] } } }
```
Use one build per theme/brand to generate separate outputs.
5. **Publish:** versioned package (npm / Maven / SPM) via Changesets (`creative-arts.design-for-form-and-experience.design-systems.versioning-deprecating-and-changelogging`); apps update through Renovate PRs.
6. **Test:** snapshot token output; visual regression of key components.

## Verify
- [ ] One source of truth; every token change goes through a PR.
- [ ] CI validates references and contrast; builds all platforms and themes.
- [ ] Packages are versioned and consumed by automated updates.
