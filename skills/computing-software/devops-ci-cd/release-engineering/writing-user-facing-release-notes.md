---
id: computing-software.devops-ci-cd.release-engineering.writing-user-facing-release-notes
name: writing-user-facing-release-notes
category: computing-software
field: devops-ci-cd
product: release-engineering
tags: [release-engineering, user-facing-release-notes, release-notes, changelog, keep-a-changelog, breaking-changes, upgrade-guide]
level: practitioner
status: docs-checked
description: "Write release notes users actually read: audience-first structure, breaking changes and migration steps up top, turning PR titles into benefits, and automating the draft."
sources:
  - https://keepachangelog.com/en/1.1.0/
  - https://docs.github.com/en/repositories/releasing-projects-on-github/automatically-generated-release-notes
  - https://developers.google.com/style
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Writing user-facing release notes

A changelog generated from commits is for maintainers. Release notes are for users deciding whether to upgrade and what will break.

## Structure
```markdown
# v3.2.0 (2026-10-14)

## Action required
- **Node 18 is no longer supported.** Upgrade to Node 20+ before installing. (#1234)
- `config.timeout` is now in milliseconds, not seconds. Multiply existing values by 1000. [Migration guide](...)

## New
- Export reports to CSV from the Reports page. Previously only PDF was available.
- Bulk-invite up to 500 users at once from a CSV file.

## Improved
- Dashboard loads faster for accounts with more than 10,000 records (state the measured before and after).

## Fixed
- Scheduled exports no longer skip the last day of the month. (#1301)

## Deprecated
- The `/v1/reports` endpoint will be removed in v4.0 (Q2 2027). Use `/v2/reports`.

## Security
- Fixed an XSS issue in comment rendering (CVE-2026-12345). All users should upgrade.
```
Order by what the reader must act on: breaking and security first, then value, then fixes.

## Writing rules
- Describe the effect on the user, not the implementation: "Search results now include archived projects" not "Refactor SearchService query builder".
- One item, one change; link the issue/PR for detail.
- Use the product's UI names, exact config keys, and version numbers.
- Every breaking change gets: what changed, who is affected, what to do, and an example.
- Quantify improvements only with measured numbers.
- Leave out internal refactors, CI changes and dependency bumps unless they affect users (security, minimum versions).

## Automating the draft
- PR labels feed GitHub's generated release notes, configured by `.github/release.yml` categories; other tools can draft notes from commit messages or change files.
```yaml
# .github/release.yml
changelog:
  exclude: { labels: [skip-changelog, dependencies] }
  categories:
    - { title: Action required, labels: [breaking-change] }
    - { title: New, labels: [feature] }
    - { title: Fixed, labels: [bug] }
```
- A human edits the draft before publishing: merge related items, rewrite titles as benefits, add migration notes.
- Require a "release note" field in the PR template for user-visible changes so the raw material exists.

## Distribution
Same content in GitHub Releases, docs site changelog page, in-app "What's new", and the upgrade guide for majors. Keep the version history permanently available.

## Verify
- [ ] A user can tell from the first screen whether they must change anything to upgrade.
- [ ] Every item maps to a merged PR; no internal-only noise.

## Checked

2026-10-28. Confirmed against GitHub's automatically generated release notes page: `.github/release.yml` with `changelog.exclude.labels` and `changelog.categories[*].title` / `labels`; and Keep a Changelog (change-type headings). Removed: the percentage figure in the example and the release-drafter, release-please and changesets details.

Method: documentation only; no commands were run.
