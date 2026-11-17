---
id: computing-software.devops-ci-cd.nx.nx-conformance-cloud-publish
name: nx-conformance-cloud-publish
category: computing-software
field: devops-ci-cd
product: nx
tags: [nx, conformance, nx-cloud, enterprise, publish-conformance-rules, bundle-rules]
level: advanced
status: docs-checked
description: "Publish custom Nx Conformance rules to Nx Cloud Enterprise: create-rule, bundle-rules executor, nx-cloud publish-conformance-rules, publish target wiring."
sources:
  - https://raw.githubusercontent.com/nrwl/nx/master/astro-docs/src/content/docs/enterprise/publish-conformance-rules-to-nx-cloud.mdoc
  - https://raw.githubusercontent.com/nrwl/nx/master/astro-docs/src/content/docs/enterprise/conformance.mdoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: share custom conformance rules across workspaces without a private npm registry (Nx Cloud Enterprise).

1. Create a library to hold rules, and add the plugin if missing:
```shell
nx generate @nx/js:library cloud-conformance-rules
nx add @nx/conformance
nx g @nx/conformance:create-rule --name=test-cloud-rule --directory=cloud-conformance-rules/src --category=reliability --description="A test cloud rule" --reporter=non-project-files-reporter
```
Layout required: one named subdirectory per rule under `src/`, each with `index.ts` and `schema.json`. Delete the generated `lib` directory.

2. Replace the project's build target with the bundler:
```jsonc
// cloud-conformance-rules/project.json
"targets": {
  "build": {
    "executor": "@nx/conformance:bundle-rules",
    "outputs": ["{options.outputPath}"],
    "options": { "outputPath": "{projectRoot}/dist" }
  },
  "publish": {
    "dependsOn": ["build"],
    "command": "npx nx-cloud publish-conformance-rules {projectRoot}/dist"
  }
}
```
`nx build cloud-conformance-rules` outputs one subdirectory per rule with bundled `index.js` and `schema.json`.

3. Publish: `nx publish cloud-conformance-rules` (or directly `nx-cloud publish-conformance-rules cloud-conformance-rules/dist`; the output path is the first positional argument).

Behaviour:
- Re-publishing overwrites that rule's artifacts (implementation and schema). Rules are always "at HEAD": no explicit versions, so handle version differences inside the rule at runtime.
- Consume them by running `nx-cloud conformance:check` in CI (see nx-conformance-rules); the nx-cloud CLI handles authentication and merges cloud-configured rules with local ones.

## Checked

2026-11-07. Confirmed: the publish steps and rule configuration against the Publish conformance rules page; nx-cloud conformance:check against the Conformance page (added to sources). Removed: an invented Verify step.

Method: documentation only; no commands were run.
