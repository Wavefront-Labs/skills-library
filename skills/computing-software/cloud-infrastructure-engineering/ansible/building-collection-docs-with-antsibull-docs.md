---
id: computing-software.cloud-infrastructure-engineering.ansible.building-collection-docs-with-antsibull-docs
name: building-collection-docs-with-antsibull-docs
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, collection-development, antsibull-docs, docs-build, sphinx, collection-docs, github-pages, plugin-documentation]
level: advanced
status: docs-checked
description: "Generate an HTML documentation site for a collection with antsibull-docs and Sphinx, lint plugin docs, add extra docs pages, and publish from CI to GitHub Pages."
sources: ["antsibull-docs collection documentation (https://github.com/ansible-community/antsibull-docs/blob/main/docs/collection-docs.md)", "Documenting collections (https://docs.ansible.com/ansible/latest/dev_guide/developing_collections_documenting.html)", "github-docs-build (https://github.com/ansible-community/github-docs-build)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Building collection docs with antsibull-docs

Goal: the same rendered module/plugin pages users see on docs.ansible.com, built for your own
(private or public) collection, failing CI when docs are malformed.

## 1. Lint the docs first
```bash
pip install antsibull-docs
antsibull-docs lint-collection-docs --plugin-docs --skip-rstcheck .   # run from the collection root
```
`--plugin-docs` validates the schemas and markup of module, plugin and role docs; `--skip-rstcheck` skips the optional rstcheck pass over the generated RST. Add `--check-extra-docs-refs` to check references in extra docs and `--validate-collection-refs {self,dependent,all}` to validate cross-references such as `M()` and `O()`. The `validate-modules` sanity test in `ansible-test` also validates plugin docs but does not check filter and test plugins or cross-references, so run both.

## 2. Build a site
```bash
mkdir -p build-docs
antsibull-docs sphinx-init --use-current --squash-hierarchy --dest-dir build-docs acme.platform
cd build-docs
pip install -r requirements.txt     # sphinx, sphinx-ansible-theme
./build.sh                          # writes build/html
```
`--use-current` assumes the collection is already installed (without it antsibull-docs installs the collection temporarily); installing it yourself and always passing `--use-current` is recommended. `--squash-hierarchy` avoids the extra tree level for a single-collection site. In CI add `--fail-on-error` so parsing and schema errors fail the build; `--lenient` relaxes Sphinx while you are getting the first build to pass.

## 3. Extra pages and links
```yaml
# docs/docsite/extra-docs.yml
sections:
  - title: Guides
    toctree:
      - getting_started
      - upgrading_to_v3
# docs/docsite/rst/getting_started.rst holds the page
```
Labels in these RST files must be prefixed `ansible_collections.<namespace>.<name>.docsite.`.
```yaml
# docs/docsite/links.yml
edit_on_github: {repository: acme/ansible-collection-platform, branch: main, path_prefix: ""}
extra_links: [{description: Report an issue, url: "https://github.com/acme/ansible-collection-platform/issues"}]
# the issue tracker, homepage and repository links are also added automatically from galaxy.yml
```

## 4. CI publish
The `ansible-community/github-docs-build` repository provides GitHub actions and reusable workflows for generating collection docs on GitHub, or run steps 1-2 in any CI and upload `build/html` as a static site. Fail the PR on `lint-collection-docs` errors.

## Gotchas
- Install the collections your collection depends on before building, so cross-references can resolve.
- The changelog page needs `changelogs/changelog.yaml` (antsibull-changelog) and `write_changelog: true` in the antsibull-docs config.

## Verify
- [ ] `lint-collection-docs` exits 0 in CI.
- [ ] Built site lists every module/plugin under `plugins/` with options and examples; links to other plugins resolve.

## Checked

Checked 2026-10-26 against the antsibull-docs `docs/collection-docs.md` (main branch, repository active 2026-10-24) and the github-docs-build README. Confirmed: `lint-collection-docs` options `--plugin-docs`, `--skip-rstcheck`, `--check-extra-docs-refs`, `--validate-collection-refs`; `sphinx-init` options `--use-current`, `--squash-hierarchy`, `--fail-on-error`, `--lenient`, default sphinx-ansible-theme, `build.sh` output `build/html`; `extra-docs.yml` and `links.yml` layout; changelog needs `write_changelog`. Removed unconfirmed claims about empty option tables, private hub rendering and GitHub Pages publishing.

Method: documentation only; no commands were run.
