---
id: computing-software.web-development.bun.link-local-packages
name: link-local-packages
category: computing-software
field: web-development
product: bun
tags: [bun-link, link-protocol, local-development, unlink]
level: practitioner
status: docs-checked
description: "Develop against a local package with bun link, bun unlink and the link: dependency protocol, including path rules and what link does not install."
sources:
  - https://raw.githubusercontent.com/oven-sh/bun/main/docs/pm/cli/link.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
```bash
cd /path/to/cool-pkg && bun link          # register
cd /path/to/my-app && bun link cool-pkg   # symlink into node_modules
bun link --save cool-pkg                  # adds "cool-pkg": "link:cool-pkg"
cd /path/to/cool-pkg && bun unlink        # unregister
```

Link by path, no registration needed:

```json
{ "dependencies": { "shared": "link:../shared", "tokens": "link:./vendor/tokens" } }
```

Gotchas:
- Paths resolve relative to the declaring `package.json`.
- `link:dir` and `link:@scope/dir` are read as registered names; write `link:./dir` for a directory.
- The directory must exist but needs no `package.json`; its own dependencies are not installed. Use `file:` for a copy with dependencies, or make it a workspace.
- Only your project may use a `link:` path (root or workspace `package.json`, top-level `overrides`). If a registry, git or tarball package declares one, `bun install` fails.

## Checked

2026-11-04. Confirmed against bun docs pm/cli/link.mdx: bun link, link --save, bun unlink, link: path rules, registered-name ambiguity, directory requirements, not installing the directory's dependencies, who may declare a link: path.

Method: documentation only; no commands were run.
