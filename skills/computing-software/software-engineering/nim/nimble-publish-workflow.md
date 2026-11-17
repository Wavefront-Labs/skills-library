---
id: computing-software.software-engineering.nim.nimble-publish-workflow
name: nimble-publish-workflow
category: computing-software
field: software-engineering
product: nim
tags: [nimble-publish-workflow, nimble-publishing, nimble-publish, publish, package-list, packages-json, release, git-tag, github, nim]
level: practitioner
status: docs-checked
description: "Release a Nimble package by tagging a version and register its name with nimble publish or a pull request to the nim-lang/packages repository."
sources:
  - https://github.com/nim-lang/nimble/blob/master/nimble-guide/docs/create-packages.md
  - https://github.com/nim-lang/nimble/blob/master/nimble-guide/docs/use-packages.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# nimble publish and the package list

Goal: make a package installable by name.

- Publishing is optional; it associates a name with a URL in the official packages repository (`github.com/nim-lang/packages`, whose `packages.json` lists all published packages).
- Two ways: semi-automatic `nimble publish`, which needs a GitHub account with a personal access token (stored in `$nimbleDir/github_api_token`; replace that file to change the token), or manually fork the packages repository, add an entry to `packages.json` and open a pull request. This is done once, not per version.
- Release a version by creating a tag in the Git or Mercurial repository: 1) increment `version` in the .nimble file, 2) commit, 3) tag (for example `git tag v0.2.0`), 4) push tags and commits. Nimble then sees the new version.
- Tag labels use dot-separated numbers; the guide's examples: `v0.2.0` is 0.2.0, `v1` is 1, `v1.2.3-zuzu` is 1.2.3, `foo-1.2.3.4` is 1.2.3.4.
- Nimble installs the latest tagged version; with no tags it installs the latest commit.
- Before the package is accepted, install by URL: `nimble install https://github.com/user/pkg` (Git or Mercurial; `?subdir=<path>` selects a package in a subdirectory).
- `nimble search <fragment-or-tag>` lists matching packages; `nimble refresh` updates the local package list.

Gotchas:
- Bump `version` before tagging, never after.
- Never commit the access token; Nimble keeps its own copy in `$nimbleDir`.

Verify: `nimble search pkg` finds the package once the registry entry is merged.

## Checked

2026-11-03. Confirmed in the Nimble guide pages "Creating Nimble packages" (publish, token file, release steps, tag formats) and "Using packages" (URL install, `?subdir`, tags/HEAD rule, search, refresh). Removed: prerequisites list (LICENSE/README), the metadata field list of a registry entry, and "a tag without a matching version confuses nimble" (not stated).
Method: documentation only; no commands were run.
