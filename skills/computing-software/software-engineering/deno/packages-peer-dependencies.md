---
id: computing-software.software-engineering.deno.packages-peer-dependencies
name: packages-peer-dependencies
category: computing-software
field: software-engineering
product: deno
tags: [packages, peer-dependencies, node-modules-linker, hoisted, optional-peers, unmet-peers]
level: advanced
status: docs-checked
description: "How Deno resolves npm peer dependencies, why deno.json has no peerDependencies, the hoisted linker, optional peers, and fixing unmet peers."
sources:
  - https://raw.githubusercontent.com/denoland/docs/main/runtime/packages/peer_dependencies.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`peerDependencies` is a `package.json` field and the only place Deno reads peers from. `deno.json` has no equivalent; `imports` is an import map, not a manifest. To author a package needing peers, use package.json. When consuming, Deno reads an npm package's peers and resolves them from your graph.

Provide a peer by making it resolvable next to the package that needs it:

```json title="deno.json"
{
  "imports": {
    "react": "npm:react@^19",
    "some-react-plugin": "npm:some-react-plugin@^1"
  }
}
```

In a package.json project, list `react` in `dependencies`.

Layout: in the default isolated `node_modules` layout, each package sees only what it declares, so the project must provide peers. If a package walks `node_modules` expecting a flat (hoisted) sibling, use the hoisted linker, which needs a manually managed directory:

```json title="deno.json"
{
  "nodeModulesDir": "manual",
  "nodeModulesLinker": "hoisted"
}
```

Optional peers are marked via `peerDependenciesMeta` (`{ "react": { "optional": true } }`); provide them only if you use the feature needing them.

An unmet peer shows as a module-not-found error for the missing package. Add it to your dependencies and run `deno install`.

## Checked

2026-11-04. Confirmed against the Deno Peer dependencies page: package.json-only peerDependencies, providing peers via imports, isolated versus hoisted layout and the `nodeModulesLinker` config, optional peers, unmet-peer fix. Nothing removed.

Method: documentation only; no commands were run.
