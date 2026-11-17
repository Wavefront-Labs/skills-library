---
id: media-communication.technical-writing.docs-as-code.mkdocs-site-with-ci-publishing
name: mkdocs-site-with-ci-publishing
category: media-communication
field: technical-writing
product: docs-as-code
tags: [docs-as-code, mkdocs, mkdocs-material, sphinx, docusaurus, asciidoc, antora, markdown, static-site-generator, github-actions, ci, github-pages, versioned-docs, mike, link-checking, vale, pull-request-review, docs-pipeline, nav, redirects, migration, readthedocs, documentation-site]
level: practitioner
status: docs-checked
description: "Set up a docs-as-code site: choose a generator (MkDocs, Sphinx, Docusaurus, AsciiDoc), build with strict checks in CI, publish versioned docs and migrate."
sources:
  - https://www.mkdocs.org/user-guide/cli/
  - https://squidfunk.github.io/mkdocs-material/setup/setting-up-versioning/
  - https://github.com/jimporter/mike
  - https://docusaurus.io/docs/versioning
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MkDocs site with CI publishing (docs-as-code)

**Goal:** documentation written in plain-text files in git, reviewed in pull requests,
checked and built automatically, and published — with versions — on every merge.
MkDocs is the worked example; the same pipeline shape applies to Sphinx, Docusaurus and
Antora/AsciiDoc.

## 1. Pick the generator
| Tool | Source | Best for |
|---|---|---|
| MkDocs (+ Material theme) | Markdown, YAML config | Fast, simple product/internal docs |
| Sphinx | reStructuredText or Markdown (MyST) | Python projects, API autodoc, PDF output |
| Docusaurus | MDX (Markdown + React) | JS teams wanting React components, built-in versioning |
| Antora / Asciidoctor | AsciiDoc | Large multi-repo docs, complex reuse |
Choose by team skills and needs (versioning, reuse, PDF), not novelty.

## 2. Minimal MkDocs project
```bash
pip install mkdocs-material   # pin versions in requirements.txt
mkdocs new .
```
```yaml
# mkdocs.yml
site_name: Example Docs
site_url: https://docs.example.com/
repo_url: https://github.com/<ORG>/<REPO>
theme:
  name: material
nav:
  - Home: index.md
  - Get started: get-started.md
  - Guides:
      - Export data: guides/export.md
```
- `mkdocs serve` for live preview; `mkdocs build --strict` aborts the build on any
  warning — use `--strict` in CI always.
- Keep docs next to code (`/docs` in the product repo) when developers contribute;
  separate repo when writers own everything.

## 3. CI pipeline (GitHub Actions example)
On pull requests: build strictly, lint prose, check links. On merge to main: deploy.
```yaml
name: docs
on: {pull_request: {}, push: {branches: [main]}}
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@<PINNED_MAJOR>
        with: {fetch-depth: 0}
      - uses: actions/setup-python@<PINNED_MAJOR>
        with: {python-version: "<PYTHON_VERSION>"}
      - run: pip install -r requirements.txt
      - run: mkdocs build --strict
      # optional: prose lint (vale) and external link check (lychee-type tool)
      - if: github.ref == 'refs/heads/main'
        run: mkdocs gh-deploy --force
```
`gh-deploy` deploys the built site to GitHub Pages (`--force` forces the push); the job
needs write permission to contents. *Action versions move; pin to current majors.* Alternatives:
Read the Docs (builds on its side), Netlify/Vercel/Cloudflare Pages previews per PR —
**PR previews** are worth it so reviewers see rendered pages.

## 4. Versioned docs
- MkDocs: the **mike** tool keeps each version in its own directory on the deploy branch with
  a version selector (`mike deploy --push --update-aliases 2.1 latest`, `mike set-default
  --push latest`). Material supports mike's selector via `extra.version.provider: mike`.
- Docusaurus: `npm run docusaurus docs:version 2.1` snapshots the docs folder.
- Sphinx: usually via Read the Docs versions (from git tags/branches).
- Only keep versions you support; mark old ones with a banner.

## 5. Writing workflow
- Every change via PR; CODEOWNERS routes docs PRs to writers and subject experts.
- Docs updates in the same PR as the code change ("no docs, no merge" for user-facing changes).
- Include snippets from real code files rather than pasting.

## 6. Migrating between generators
1. Inventory pages and URLs (crawl the old site/sitemap).
2. Convert source (pandoc for rST/AsciiDoc ↔ Markdown; then hand-fix admonitions, tabs,
   cross-references — these never convert cleanly).
3. Keep URLs or add redirects (a redirects plugin, or host-level redirects).
4. Build strictly, check links, compare page counts old vs new.

## Gotchas
- Forgetting `--strict`: broken links ship silently.
- Nav defined both in `mkdocs.yml` and by plugins → confusing ordering; pick one.

## Checked
2026-11-01. Confirmed: `mkdocs build --strict` aborts on warnings; `gh-deploy` and `--force` exist (MkDocs CLI page); mike `deploy --push --update-aliases 2.1 latest`, `set-default --push latest`, per-version directories (mike README); `extra.version.provider: mike` (Material versioning page); `npm run docusaurus docs:version` snapshots `docs/` (Docusaurus versioning). Removed: Material feature names, markdown extension list, snippets and redirects plugin names, shallow-clone claim, pinned action and Python versions, gh-pages branch name.
Method: documentation only; no commands were run.

## Verify
- [ ] `mkdocs build --strict` passes locally and in CI.
- [ ] A PR with a broken internal link fails CI.
- [ ] Merging to main updates the live site within minutes.
- [ ] Version selector shows supported versions; default is latest.
- [ ] After a migration, old URLs redirect and page counts match.
