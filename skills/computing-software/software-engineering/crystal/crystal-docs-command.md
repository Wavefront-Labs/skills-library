---
id: computing-software.software-engineering.crystal.crystal-docs-command
name: crystal-docs-command
category: computing-software
field: software-engineering
product: crystal
tags: [crystal-docs-command, cli-spec-docs-format, crystal-docs, api-docs, doc-generator, project-name, project-version, source-refname, json-docs, crystal]
level: practitioner
status: docs-checked
description: "Generate API docs with crystal docs: output dir, project name and version defaults, source link options, html or json format, :nodoc: and :ditto:."
sources:
  - https://github.com/crystal-lang/crystal-book/blob/master/docs/man/crystal/README.md
  - https://github.com/crystal-lang/crystal/blob/master/src/compiler/crystal/command/docs.cr
  - https://github.com/crystal-lang/crystal-book/blob/master/docs/syntax_and_semantics/documenting_code.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# crystal docs and API documentation

Goal: publish docs.

- `crystal docs [--output=<dir>] [--canonical-base-url=<url>] [<source_file>...]` writes a static site (default `./docs`) with an HTML file per type; open `docs/index.html`. The whole API is also stored as JSON in `index.json` in the output directory.
- By default all files in `./src` are appended (`src/**/*.cr`); pass entrypoint files if load order matters.
- Options: `--project-name=NAME` and `--project-version=VERSION` (defaults come from `shard.yml`, the version also from the current git commit; mandatory if no default is found), `--source-refname=REFNAME` (git tag or commit hash for source links), `--source-url-pattern`, `-o DIR` / `--output=DIR`, `-f FORMAT` / `--format=FORMAT` (`html` or `json`), `--canonical-base-url=URL`, `-b URL` / `--sitemap-base-url=URL`, `--json-config-url=URL`, `--base-path=PATH`.
- `# :nodoc:` hides a public feature; private and protected features are always hidden unless `# :showdoc:` is used. `# :ditto:` reuses the previous feature's documentation.

Gotchas:
- If no name or version can be determined, the command asks for `--project-name` / `--project-version`.

Verify: open `docs/index.html` and check that the project name and version are right.

## Checked

2026-11-03. Confirmed against the Crystal compiler manual (`crystal docs` synopsis, defaults, output files), the `docs` command source (option names and the `html`/`json` formats) and the "Documenting code" page (`:nodoc:`, `:showdoc:`, `:ditto:`).
Removed: the claim that stdlib API docs are built the same way, "code blocks in docs are not run" and "wrong refname gives broken source links".
Method: documentation only; no commands were run.
