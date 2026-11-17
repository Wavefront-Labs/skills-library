---
id: computing-software.software-engineering.crystal.shards-doc-publishing
name: shards-doc-publishing
category: computing-software
field: software-engineering
product: crystal
tags: [shards-doc-publishing, doc-comments, publish, release, github-pages, semver, tag, readme, ci-docs, crystal]
level: practitioner
status: docs-checked
description: "Release a Crystal shard: bump version, tag as vX.Y.Z so Shards resolves it, set the crystal constraint, and generate API docs with crystal docs."
sources:
  - https://github.com/crystal-lang/shards/blob/master/docs/shard.yml.adoc
  - https://github.com/crystal-lang/crystal-book/blob/master/docs/guides/writing_shards.md
  - https://github.com/crystal-lang/crystal-book/blob/master/docs/man/crystal/README.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Publishing docs and releasing a shard

Goal: ship a library.

- Bump `version:` in shard.yml and create a git tag `vX.Y.Z`. Shards reads versions from tags matching `v<version>`; tags without the leading `v` are ignored for version resolution.
- Follow a rational scheme such as Semantic Versioning or Calendar Versioning (Shards does not enforce one); `~>` constraints in dependents rely on it.
- Docs: `crystal docs` writes HTML to `./docs` (entrypoint `docs/index.html`) and the full API as JSON in `index.json`. `--project-name` and `--project-version` default from shard.yml (version also from the current git commit); `--output` and `--canonical-base-url` are also available.
- `crystal docs` documents `src/**/*.cr` by default.
- A library should state its supported Crystal versions in the `crystal:` field, with an upper bound below the next major Crystal version if you want to be safe.
- README: show the `dependencies:` snippet, the `require`, and minimal usage.
- Library `shard.lock` is not committed (applications commit it).

Gotchas:
- A dependent with no tag to resolve gets HEAD (or the branch/commit it pins), not a release.

Verify: in a scratch project, `shards install` resolves your new tag.

## Checked

2026-11-03. Confirmed against shard.yml(5) (tag pattern `v<version>`, `crystal:` field, versioning advice, resolver fallbacks), shards(1) (library lock rule) and the Crystal compiler manual `crystal docs` section.
Removed: the claim that a leading `v` is merely "accepted" (it is required for resolution), Shardbox and GitHub topic discovery, `--source-refname` and GitHub Pages CI steps (not in the pages read here), "keep a CHANGELOG", and "test on the oldest supported version".
Method: documentation only; no commands were run.
