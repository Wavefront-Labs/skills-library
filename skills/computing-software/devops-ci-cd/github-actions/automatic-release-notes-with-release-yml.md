---
id: computing-software.devops-ci-cd.github-actions.automatic-release-notes-with-release-yml
name: automatic-release-notes-with-release-yml
category: computing-software
field: devops-ci-cd
product: github-actions
tags: [github-actions, generate-release-notes, release-yml, release-notes-categories, changelog-labels]
level: intro
status: docs-checked
description: "Configure GitHub's automatically generated release notes with .github/release.yml: label categories, exclusions, and calling the generate-notes API from workflows."
sources: ["https://docs.github.com/en/repositories/releasing-projects-on-github/automatically-generated-release-notes", "https://docs.github.com/en/rest/releases/releases#generate-release-notes-content-for-a-release"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Automatic release notes and `.github/release.yml`

Generated notes list merged PRs since the previous release, contributors, and a "Full Changelog"
compare link. `release.yml` turns that flat list into sections.

## 1. Config
```yaml
# .github/release.yml
changelog:
  exclude:
    labels: [ignore-for-release, chore]
    authors: [dependabot, renovate]
  categories:
    - title: Breaking changes
      labels: [breaking-change, semver-major]
    - title: Features
      labels: [enhancement, feature]
    - title: Fixes
      labels: [bug]
    - title: Dependencies
      labels: [dependencies]
    - title: Other changes
      labels: ["*"]          # catch-all
```
`labels: "*"` is the catch-all category; it is required to display PRs that matched no other category.

## 2. Use it
- UI: when drafting a release, optionally pick the **Previous tag**, then generate the notes.
- CLI: `gh release create v1.3.0 --generate-notes [--notes-start-tag v1.2.0]`.
- API (preview the text without creating a release):
```bash
gh api -X POST /repos/$R/releases/generate-notes \
  -f tag_name=v1.3.0 -f previous_tag_name=v1.2.0 -f target_commitish=main -q .body
```
`configuration_file_path` points the API at another config file; by default `.github/release.yml` or `.github/release.yaml` is used, then the built-in default.

## 3. Make it work in practice
- The notes list merged pull requests, so category labels must be on the PRs.
- To set the range yourself, pass `previous_tag_name` (API) or `--notes-start-tag` (`gh release create`).

## Verify
- [ ] Preview via the API shows every merged PR under a category; nothing under an unexpected heading.

## Checked

2026-10-31. Confirmed against the GitHub automatically generated release notes page, the REST releases page and the gh source: .github/release.yml keys (changelog.exclude.labels, changelog.exclude.authors, changelog.categories[*].title and .labels, `*` catch-all), the generate-notes endpoint and its tag_name, target_commitish, previous_tag_name and configuration_file_path parameters and default config path, and gh release create --generate-notes and --notes-start-tag.
Removed: the default-branch requirement, first-match category and catch-all-must-be-last claims, the Generate release notes button name, third-party label-enforcement actions and the squash-title and backport-tag gotchas.

Method: documentation only; no commands were run.
