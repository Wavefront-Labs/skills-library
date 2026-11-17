---
id: computing-software.web-development.bun.pm-pack-and-version
name: pm-pack-and-version
category: computing-software
field: web-development
product: bun
tags: [bun-pm-pack, bun-pm-version, version-bump, npm-pack]
level: practitioner
status: docs-checked
description: "Create a publishable tarball with bun pm pack and bump versions with bun pm version, including git tag behaviour and npm_new_version in scripts."
sources:
  - https://raw.githubusercontent.com/oven-sh/bun/main/docs/pm/cli/pm.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Pack (follows `npm pack` rules):

```bash
bun pm pack --dry-run                # no file written
bun pm pack --destination ./out
bun pm pack --filename pkg.tgz       # cannot combine with --destination
bun pm pack --ignore-scripts --gzip-level 6 --quiet   # --quiet prints only the filename
```

Version bump:

```bash
bun pm version patch                 # minor|major|premajor|preminor|prepatch|prerelease|from-git|<x.y.z>
bun pm version prerelease --preid beta
bun pm version minor --no-git-tag-version
bun pm version patch -m "release %s" # %s is the version
bun pm version patch --dry-run
```

Gotchas:
- By default it creates a git commit and tag; `--no-git-tag-version` skips them. `--allow-same-version` prevents an error when the version is unchanged; `--force` (`-f`) bypasses the dirty git history check.
- Increments match `npm version`: on `1.0.0-rc.1`, `major` yields `1.0.0`.
- Scripts see `$npm_old_version` and `$npm_new_version`; `$npm_package_version` is the old version in `preversion` and the new one afterward.

## Checked

2026-11-04. Confirmed against bun docs pm/cli/pm.mdx: pack options and the --filename/--destination exclusion, version increments and options, git commit and tag default, npm version parity, npm_old_version and npm_new_version. Reworded the override flags to what the page says each does.

Method: documentation only; no commands were run.
