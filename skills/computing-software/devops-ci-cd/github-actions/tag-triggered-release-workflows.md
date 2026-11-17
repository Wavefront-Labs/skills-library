---
id: computing-software.devops-ci-cd.github-actions.tag-triggered-release-workflows
name: tag-triggered-release-workflows
category: computing-software
field: devops-ci-cd
product: github-actions
tags: [github-actions, tag-push-trigger, release-on-tag, semver-tag-filter, tag-on-main-check]
level: practitioner
status: gated
description: "Trigger release builds from tag pushes safely: tag filters, ref_name, prerelease detection, checking the tag is on main, and the 3-tag and GITHUB_TOKEN trigger limits."
sources: ["https://docs.github.com/en/actions/writing-workflows/workflow-syntax-for-github-actions#onpushbranchestagsbranches-ignoretags-ignore", "https://docs.github.com/en/actions/writing-workflows/choosing-when-your-workflow-runs/events-that-trigger-workflows#push"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tag-triggered release builds

## 1. Trigger
```yaml
on:
  push:
    tags: ['v[0-9]+.[0-9]+.[0-9]+', 'v[0-9]+.[0-9]+.[0-9]+-*']
```
Glob syntax, not regex: `+` means "one or more of the preceding char", `[0-9]` works, `*` does not
match `/`. A bare `v*` also matches `very-bad-tag`.
`github.ref` = `refs/tags/v1.2.3`, `github.ref_name` = `v1.2.3`, `github.ref_type` = `tag`.

## 2. Guard rails in the job
```yaml
jobs:
  release:
    runs-on: ubuntu-latest
    permissions: { contents: write }
    steps:
      - uses: actions/checkout@v4
        with: { fetch-depth: 0 }
      - name: Tag must point at a commit on main
        run: git merge-base --is-ancestor "$GITHUB_SHA" origin/main
      - name: Tag must match the version file
        run: test "${GITHUB_REF_NAME#v}" = "$(jq -r .version package.json)"
      - id: kind
        run: echo "prerelease=${{ contains(github.ref_name, '-') }}" >> "$GITHUB_OUTPUT"
```
Protect tags with a repository tag ruleset restricting who can create, update or delete `v*` tags (see GitHub's rulesets docs for the exact options).

## 3. Surprises
- Tags pushed with `GITHUB_TOKEN` (e.g. by semantic-release in another workflow) do **not**
  trigger this workflow (gated: unconfirmed, source is paywalled or blocked) — push with a GitHub App token, or call the release workflow directly.
- Pushing more than **three tags at once** creates no push events (`git push --tags` after a
  backlog) — push tags individually.
- The workflow file used is the version at the tagged commit (gated: unconfirmed, source is paywalled or blocked); if release.yml was fixed on main, an old tag may need re-tagging or a `workflow_dispatch` run with a tag input.
- Annotated vs lightweight both trigger (gated: unconfirmed, source is paywalled or blocked); `actions/checkout` defaults to a shallow fetch, so `git describe` needs `fetch-depth: 0` (see the checkout README).
- Deleting and re-pushing the same tag re-runs the release; with immutable releases it fails instead.

## Verify
- [ ] `git tag v0.0.0-test && git push origin v0.0.0-test` runs the workflow as a prerelease.
- [ ] A tag on a feature branch fails the "on main" step.

## Checked

2026-11-02. Confirmed from GitHub's workflow syntax and events pages: tag filter glob rules (* does not match /, + means one or more of the preceding character), github.ref_name and github.ref_type values, and that no push event is created when more than three tags are pushed at once. Removed the specific ruleset permission wording. Gated: GITHUB_TOKEN-pushed tags not triggering workflows, the tagged-commit workflow-file rule, annotated/lightweight behaviour and checkout fetch depth, plus git merge-base --is-ancestor, git describe and git push --tags options (git docs fetched but those lines not individually reviewed).

Method: documentation only; no commands were run.
