---
id: computing-software.web-development.biome.linter-domains-framework-and-project-rules
name: linter-domains-framework-and-project-rules
category: computing-software
field: web-development
product: biome
tags: [biome, linter-domains, react-domain, test-domain, project-domain, scanner, module-graph, no-floating-promises, no-import-cycles]
level: advanced
status: docs-checked
description: "Enable rule domains by detected dependencies or config, and understand how project-domain rules trigger the Scanner and its performance cost."
sources:
  - https://raw.githubusercontent.com/biomejs/website/main/src/content/docs/en/linter/index.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
**Domains** group rules by technology (examples: `react`, `solid`, `test`). A domain has its own recommended rules, can be enabled automatically when certain dependencies appear in the nearest `package.json` (for example detecting `mocha` enables the recommended rules of the `test` domain), and can define extra global variables.

Without a `package.json`, or when auto-detection does not apply, set it in config. Values are `"recommended"`, `"all"` and `"none"`:

```json
{ "linter": { "domains": { "test": "recommended" } } }
```

**The Scanner (Biome v2).** The Scanner crawls project files to build the module graph and inferred types. Rules such as `noFloatingPromises`, `noUnresolvedImports` and `noImportCycles` need this and belong to the **project** domain. The Scanner is **opt-in**: it runs only when a project-domain rule is enabled. Measured by the team: about 2k files ~800ms without vs ~2s with it; about 5k files ~1000ms vs ~8s. The team says it is working to improve this; if numbers look abnormal, file an issue with a repository link. See the investigate-slowness guide.

**Memory.** An editor process may use much memory when a project-domain rule is on. To infer types Biome scans `.d.ts` files inside `node_modules`, including transitive dependencies, on purpose: libraries can export types that come from their own dependencies (for example `@org/foo` exporting `Validator` from `@other-org/validator`). The team is aware and plans optimisation.

## Checked

2026-11-08. Read the linter index page in full. Unchanged: domain definition and auto-detection, the recommended/all/none values, Scanner description, timings and memory explanation. Removed: advice on forcing ignores for build output (not on the page) and the invented Verify step.

Method: documentation only; no commands were run.
