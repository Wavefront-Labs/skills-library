---
id: computing-software.software-engineering.pnpm.package-json-peers-and-meta
name: package-json-peers-and-meta
category: computing-software
field: software-engineering
product: pnpm
tags: [dependencies-meta, peer-dependencies-meta, optional-peer, peer-specifier-schemes, invalid-peer-specification, injected-dependency-meta]
level: practitioner
status: docs-checked
description: "Declare peers in package.json for pnpm: allowed specifier schemes, the rejected name@version form, peerDependenciesMeta optional and dependenciesMeta injected."
sources:
  - https://pnpm.io/package_json
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`peerDependencies` values are semver ranges, `workspace:` or `catalog:` specifiers, or a scheme specifier:

```json
{
  "peerDependencies": {
    "lib-a": "work:5.x.x",
    "lib-b": "npm:other-lib@^5",
    "lib-c": "file:../lib-c",
    "lib-d": "git+https://example.com/lib-d.git"
  }
}
```

- Accepted: named-registry spec, `npm:` alias, `file:`, git, URL.
- The embedded range is what gets matched (`work:5.x.x` as `5.x.x`, `npm:other-lib@^5` as `^5`); a spec with no version matches `*`. The original specifier selects the package when `autoInstallPeers` installs a missing peer.
- Bare `"lib-a": "lib-a@1.2.3"` fails with `ERR_PNPM_INVALID_PEER_DEPENDENCY_SPECIFICATION`.

`peerDependenciesMeta.<name>.optional: true` marks a peer optional, even one not listed in `peerDependencies` (any version is assumed fine). A missing optional peer gives no warning, but an installed one that fails the range still warns.

`dependenciesMeta.<name>.injected: true` installs a local workspace dependency as a hard-linked copy in `node_modules/.pnpm` instead of a symlink, so its peers resolve per consumer (`card` on react 16, `form` on react 17). Copies must be refreshed after rebuilds: rerun `pnpm install` (for example via a `prepare` script), set `syncInjectedDepsAfterScripts`, or use pnpm-sync tools.

## Checked

2026-11-04. Confirmed peer specifier schemes, matching rules, the ERR_PNPM_INVALID_PEER_DEPENDENCY_SPECIFICATION case, peerDependenciesMeta optional and dependenciesMeta injected against pnpm.io/package_json. Removed the unsourced closing Check line.

Method: documentation only; no commands were run.
