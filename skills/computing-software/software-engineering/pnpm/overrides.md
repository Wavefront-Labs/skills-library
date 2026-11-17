---
id: computing-software.software-engineering.pnpm.overrides
name: overrides
category: computing-software
field: software-engineering
product: pnpm
tags: [overrides, override-selector, convergence-override, dependency-type-selector, override-peer, remove-dependency-override, package-extensions]
level: advanced
status: docs-checked
description: "Force dependency versions with pnpm overrides: parent selectors, wildcards, :prod/:optional/:peer, removal with -, convergence overrides, catalog references and packageExtensions."
sources:
  - https://pnpm.io/settings/dependency-resolution
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`overrides` is set at the workspace root in `pnpm-workspace.yaml`:

```yaml
overrides:
  "foo": "^1.0.0"
  "quux": "npm:@myorg/quux@^1.0.0"
  "bar@^2.1.0": "3.0.0"
  "qar@1>zoo": "2"
  "foo@1.0.0>bar": "-"
  "foo": "catalog:"
```

- `parent>dep` limits the override to that parent's dependency. `*` wildcards work on package names in both selectors.
- `-` removes the dependency.
- Default scope is dependencies, devDependencies, optionalDependencies and peerDependencies. Append `:prod`, `:optional` or `:peer` to restrict, e.g. `"@esbuild/*:optional": "-"`. Removing from `optionalDependencies` also removes a duplicate in `dependencies`.
- Peer overrides: ranges, `workspace:` and `catalog:` replace the peer range; `link:`, `file:`, `npm:` leave peers unchanged; `-` removes the peer and its `peerDependenciesMeta`.
- Convergence override `"form-data@": 4.0.6` (empty range): rewrites only edges whose declared range the exact version satisfies. Value must be an exact version (else `ERR_PNPM_INVALID_CONVERGENCE_OVERRIDE`), no parent selector, and a regular override wins. A stale one produces a warning.

`packageExtensions` adds `dependencies`, `optionalDependencies`, `peerDependencies` or `peerDependenciesMeta` to a package (name or `name@range` key):

```yaml
packageExtensions:
  react-redux@1:
    peerDependencies:
      react-dom: "*"
```

## Checked

2026-11-04. Confirmed against pnpm.io/settings/dependency-resolution: override selector forms, wildcards, - removal, dependency-type selectors, optional/dependencies dedupe, peer override rules, convergence override rules and error code, packageExtensions fields and keys. Removed: the generic closing Check line (not stated on the page).
Method: documentation only; no commands were run.
