---
id: computing-software.software-engineering.crystal.shard-yml
name: shard-yml
category: computing-software
field: software-engineering
product: crystal
tags: [shard-yml, shards, dependencies, development-dependencies, targets, crystal-version, license, github-dependency, crystal]
level: practitioner
status: docs-checked
description: "Write shard.yml: required name and version, crystal constraint, dependency resolvers and version operators, targets, executables, libraries and scripts."
sources:
  - https://github.com/crystal-lang/shards/blob/master/docs/shard.yml.adoc
  - https://github.com/crystal-lang/shards/blob/master/docs/shards.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# shard.yml structure

Goal: declare a project.

```yaml
name: myapp
version: 0.1.0
crystal: ">= 0.35, < 2.0"
license: MIT
targets:
  myapp:
    main: src/myapp.cr
dependencies:
  minitest:
    github: ysbaddaden/minitest.cr
    version: ~> 0.1.3
development_dependencies:
  other_tool:
    git: https://git.example.org/other_tool.git
    branch: main
```
- `name` and `version` are required. `name` must be unique, 50 characters or less, should be lowercase and should not contain "crystal". `version` must contain digits.
- Resolvers: `path`, `git`, `github`, `gitlab`, `bitbucket`, `codeberg`, `hg`, `fossil`. Pick one per dependency, plus `version`, `tag`, `branch` or `commit` (`bookmark` for hg). With none of those, HEAD is installed.
- `git`-style resolvers read versions from tags matching `v<version>` (for example `v1.2.3`); tags without the leading `v` are ignored for version resolution.
- `version` operators: `<`, `<=`, `>`, `>=`, `!=`, `~>`, `"*"` (default); combine with commas. `~> 2.0.3` means `>= 2.0.3 and < 2.1`; `~> 2.1` means `>= 2.1 and < 3.0`.
- `crystal:` is not used during resolution; shards warns afterwards about dependencies that do not support the current Crystal. A bare version `x.y.z` is a legacy form meaning `>= x.y.z`.
- `libraries:` (soname without extension, such as `libsqlite3`, mapped to a constraint) is purely informational. `executables:` lists files in the shard's `bin` folder, copied to the dependent project's `bin`. `scripts:` supports only `postinstall`.
- `development_dependencies` are installed for the main project only, never when the shard is a dependency.

Gotchas:
- A `path:` dependency is installed as a symlink to the local path.
- `shards check` verifies dependencies are satisfied.

Verify: `shards check` exits 0.

## Checked

2026-11-03. Confirmed against shard.yml(5) and shards(1) in the Shards repository (required attributes and name rules, `crystal` semantics, resolvers, tag pattern, version operators and `~>` examples, `libraries`, `executables`, `scripts`, `development_dependencies`, `path` symlink, `check` exit status).
Removed: the specific pins `kemal ~> 1.5.0`, `will/crystal-pg`, `manastech/webmock.cr` and `>= 1.10.0, < 2.0.0` examples (not in the docs; replaced with the doc examples), "name must match the repository folder convention", and the pointer to a "spec.md" field list.
Method: documentation only; no commands were run.
