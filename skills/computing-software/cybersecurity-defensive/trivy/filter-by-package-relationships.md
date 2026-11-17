---
id: computing-software.cybersecurity-defensive.trivy.filter-by-package-relationships
name: filter-by-package-relationships
category: computing-software
field: cybersecurity-defensive
product: trivy
tags: [pkg-relationships, direct-dependencies, indirect, workspace, root, dependency-tree]
level: advanced
status: docs-checked
description: "Limit scanning to root, workspace, direct, indirect or unknown packages with --pkg-relationships, and learn which combinations with VEX and SBOM output are unsupported."
sources:
  - https://trivy.dev/latest/docs/guide/scanner/vulnerability/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The `--pkg-relationships` flag focuses a scan on certain kinds of dependencies, for example only direct ones. Trivy defines these relationships:

1. `root`: the root package being scanned.
2. `workspace`: workspaces of the root package. Currently only `pom.xml`, `yarn.lock`, `cargo.lock` and `uv.lock` files are supported.
3. `direct`: direct dependencies of the root or workspace package.
4. `indirect`: transitive dependencies.
5. `unknown`: packages whose relationship cannot be determined.

Available relationships vary by ecosystem. To see what a project supports, produce JSON output and inspect the `Relationship` field:

```
trivy repo -f json /path/to/project
```

To scan only the root package and its direct dependencies:

```
trivy repo --pkg-relationships root,direct /path/to/project
```

By default all relationships are included.

Two cautions from the page. The flag filters the packages themselves, so it also changes the package list in JSON reports and SBOM generation. And because it may not provide a complete package list, `--pkg-relationships` cannot be used with `--dependency-tree`, `--vex` or SBOM generation.

## Checked

2026-11-03. Read and confirmed against the Vulnerability Scanning page on trivy.dev: the commands, flags, field names, defaults and behaviours stated above. Removed: nothing.

Method: documentation only; no commands were run.
