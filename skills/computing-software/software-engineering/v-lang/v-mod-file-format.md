---
id: computing-software.software-engineering.v-lang.v-mod-file-format
name: v-mod-file-format
category: computing-software
field: software-engineering
product: v-lang
tags: [v-mod-file-format, v-mod-and-module-search, v.mod, manifest, dependencies, version, license, module metadata, v-lang]
level: practitioner
status: docs-checked
description: "Write v.mod with name, description, version, license, dependencies and optional base_url, and know how V uses it as the module lookup root."
sources:
  - https://github.com/vlang/v/blob/master/doc/docs.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# The v.mod manifest

Goal: describe a V package.

```v
Module {
    name: 'mypackage'
    base_url: 'src'
    description: 'My nice package.'
    version: '0.0.1'
    license: 'MIT'
    dependencies: []
}
```
- `v new mypackage` or `v init` create a `v.mod`. `base_url` is optional; when set, V resolves the package sources relative to that folder, next to `v.mod`.
- Prefer a string list for `dependencies`, such as `['ui', 'nedpals.args']`. Legacy forms like `[ui: 0.1]` are accepted but only the names are kept. Dependencies may carry semver ranges such as `vsl@^0.1.47`.
- `subdirs: ['internal']` compiles selected subdirectories (relative to the module source root) as part of the same module; their files declare the same `module mypackage`.
- `backend: 'fastc'` makes builds of that project use the FastC backend by default; accepted values are `c`, `fastc`, `arm64`, `x64` and `wasm`, and an explicit `-b` wins.
- The nearest `v.mod` is the lookup root: V prepends its folder to the module lookup path so files beside or below it can import sibling modules. An empty `.v.mod.stop` file in a project root stops the upward search, and a `.git`, `.hg` or `.svn` entry stops V from selecting a parent's `v.mod`.
- Use the `module` name from the package at the top of its files. Prefer a `name` that is already a valid import path; `-` becomes `_` and names are lowercased on install.
- To publish: push to a public GitHub repository and register it at https://vpm.vlang.io/new; the final name is `githubname.mypackage`.

Gotchas:
- The syntax resembles a struct literal but is its own format.
- `v.mod` dependencies are declared by hand; `v mod why <module>` shows what pulls a module into the build.

Verify: `v install` in the project folder resolves the dependencies, then `v .` builds.

## Checked

2026-11-08. Read: the "Package management" section of doc/docs.md (vlang/v), plus the import-path lines about `v.mod` and `.v.mod.stop`. Removed unconfirmed claims: free-form versions, "no trailing commas required", the name-must-match-import gotcha as worded, and `v install --git` dependency entries. docs.vlang.io and modules.vlang.io dropped from sources.
Method: documentation only; no commands were run.
