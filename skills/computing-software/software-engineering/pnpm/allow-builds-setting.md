---
id: computing-software.software-engineering.pnpm.allow-builds-setting
name: allow-builds-setting
category: computing-software
field: software-engineering
product: pnpm
tags: [allow-builds-map, strict-dep-builds-setting, git-dependency-builds, dangerously-allow-all-builds, permissions-setting, agent-skills-dirs, migrate-only-built-dependencies]
level: practitioner
status: docs-checked
description: "Approve or deny dependency build scripts with allowBuilds: version matchers, git keys, strictDepBuilds, permissions, dangerouslyAllowAllBuilds and leaving onlyBuiltDependencies."
sources:
  - https://pnpm.io/settings/build
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
```yaml
allowBuilds:
  esbuild: true
  core-js: false
  nx@21.6.4 || 21.6.5: true
  'foo@git+ssh://git@example.com/org/foo.git': true            # any commit
  'bar@git+https://github.com/org/bar.git#abc123': true        # one commit
```

- Unlisted packages are unreviewed. With `strictDepBuilds` (default true) install exits non-zero with `ERR_PNPM_IGNORED_BUILDS`; `false` prints a warning.
- Ignored builds are added to `pnpm-workspace.yaml` with a placeholder for you to set true or false. `pnpm add --allow-build` and `pnpm approve-builds` write here too.
- A bare name never approves a git or tarball dependency. Use the repo URL key (no `#ref`) or the exact path with commit. URL schemes are matched exactly. Name denials (`foo: false`) block registry and git alike.
- A patch that adds an install script or `binding.gyp` makes the package buildable and subject to approval (v12.4.0).
- `permissions` (v12.11.0) keyed like `allowBuilds`: `build` outranks `allowBuilds`; `skills` links agent skills a package ships; `skills.dirs` sets target directories (empty list disables).
- `dangerouslyAllowAllBuilds: true` runs every build except denied ones, now and for future dependencies. Avoid.
- Removed in v11: `onlyBuiltDependencies`, `onlyBuiltDependenciesFile`, `neverBuiltDependencies`, `ignoredBuiltDependencies`, `ignoreDepScripts`. `pnpx codemod run pnpm-v10-to-v11` migrates.

## Checked

2026-11-04. Confirmed against pnpm.io/settings/build: allowBuilds examples and git-key rules, strictDepBuilds default and ERR_PNPM_IGNORED_BUILDS, patches (v12.4.0), permissions and skills.dirs (v12.11.0), dangerouslyAllowAllBuilds, removed v11 settings and the codemod. Removed: the generic closing Check line (not stated on the page).
Method: documentation only; no commands were run.
