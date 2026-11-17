---
id: computing-software.devops-ci-cd.release-engineering.git-cliff-changelog-generation
name: git-cliff-changelog-generation
category: computing-software
field: devops-ci-cd
product: release-engineering
tags: [release-engineering, git-cliff, changelog, conventional-commits, cliff-toml]
level: practitioner
status: draft
description: "Generate changelogs and next-version suggestions from conventional commits with git-cliff: cliff.toml, commit parsers, templates and CI usage."
sources: ["https://git-cliff.org/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# git-cliff changelog generation

**Goal:** a reproducible CHANGELOG built from commit history.

## Setup
```bash
git cliff --init                       # writes cliff.toml with defaults
git cliff -o CHANGELOG.md              # full history
git cliff --unreleased                 # since last tag
git cliff --latest                     # latest release only (for release notes)
git cliff --bump --unreleased          # compute next semantic version from commit types
git cliff --tag v1.4.0 -o CHANGELOG.md # label unreleased commits as a new tag
```

## cliff.toml essentials
```toml
[changelog]
header = "# Changelog\n"
body = """
{% for group, commits in commits | group_by(attribute="group") %}
### {{ group | striptags | trim | upper_first }}
{% for commit in commits %}- {{ commit.message | split(pat="\n") | first }}{% endfor %}
{% endfor %}"""
[git]
conventional_commits = true
filter_unconventional = true
commit_parsers = [
  { message = "^feat", group = "Features" },
  { message = "^fix", group = "Bug Fixes" },
  { message = "^chore\\(release\\)", skip = true },
]
```
Templates use Tera syntax. `tag_pattern` restricts which tags count as releases.

## CI
Run in the release job after tagging; use `fetch-depth: 0` (full clone with tags) or the changelog will be empty. Publish `git cliff --latest --strip header` as release notes.

## Gotchas
Squash-merge titles must follow the convention. Skip bot commits with a parser rule. Details of options vary by version; check the docs.

## Verify
Dry run on a branch (`git cliff --unreleased`) lists the commits you expect, grouped.
