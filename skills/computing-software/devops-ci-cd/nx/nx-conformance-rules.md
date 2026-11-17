---
id: computing-software.devops-ci-cd.nx.nx-conformance-rules
name: nx-conformance-rules
category: computing-software
field: devops-ci-cd
product: nx
tags: [nx, conformance, enterprise, governance, ci, nx-register, license]
level: advanced
status: docs-checked
description: "Run Nx Conformance (Enterprise): activate the license with nx register or NX_KEY, configure rules in nx.json, nx conformance vs conformance:check, CI snippets."
sources:
  - https://raw.githubusercontent.com/nrwl/nx/master/astro-docs/src/content/docs/enterprise/conformance.mdoc
  - https://raw.githubusercontent.com/nrwl/nx/master/astro-docs/src/content/docs/enterprise/activate-license.mdoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: enforce workspace-wide standards in any language with `@nx/conformance`. Needs an Nx Enterprise license.

Activate the license:
- Closed-source repo: `nx register YOUR_ACTIVATION_KEY` (one developer runs it; commit the saved file so everyone gets access), or set `NX_KEY=YOUR_ACTIVATION_KEY` in CI.
- Open-source repo: use `NX_KEY` only, never commit the key.
Nx makes no external requests for this. Without a valid license (local or via Nx Cloud) the commands fail without checking any rule.

Install: `nx add @nx/conformance`.

Configure in `nx.json`:
```jsonc
{ "conformance": { "rules": [
  { "rule": "@nx/conformance/enforce-project-boundaries",
    "options": { "depConstraints": [
      { "sourceTag": "scope:shared", "onlyDependOnProjectsWithTags": ["scope:shared"] } ] } },
  { "rule": "@nx/conformance/ensure-owners", "projects": ["!experimental-app"] },
  { "rule": "./tools/local-conformance-rule.ts" }
] } }
```
Built-in rules: Enforce Project Boundaries (every graph dependency, not just TS imports) and Ensure Owners (every project has an owner for `@nx/owners`, see nx-owners-codeowners). Local custom rules are TypeScript files referenced by path.

Commands:
- `nx conformance`: evaluates rules, applies available fix generators (not for `disabled` rules), re-evaluates to count fixed violations. Use locally.
- `nx conformance:check`: evaluate only, no fixes. Use in CI.
- `--printConfig` on either prints the resolved configuration.

CI:
```yaml
- run: npx nx conformance:check
- run: npx nx record -- npx nx conformance:check          # logs in Nx Cloud
- run: npx nx record -- npx nx-cloud conformance:check    # also applies rules configured in Nx Cloud Enterprise
```
Use the `nx-cloud` CLI form when rules are published or configured in Nx Cloud; it supplies the license automatically.

## Checked

2026-11-07. Confirmed: the rule configuration shape, projects filter and the nx conformance commands against the Conformance and Activate license pages. Removed: an invented Verify step.

Method: documentation only; no commands were run.
