---
id: computing-software.software-engineering.api-design.writing-api-changelogs
name: writing-api-changelogs
category: computing-software
field: software-engineering
product: api-design
tags: [api-design, api-changelog, api-evolution, release-notes, developer-communication, breaking-changes]
level: practitioner
status: docs-checked
description: "Keep a public API changelog: Keep a Changelog structure, a breaking versus additive classification (as GitHub's REST API documents it), advance notice and migration links."
sources: ["https://keepachangelog.com/en/1.1.0/", "https://docs.github.com/en/rest/about-the-rest-api/breaking-changes"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# API changelogs and change communication

## Entry format (Keep a Changelog 1.1.0)
- Changelogs are for humans, not machines; do not dump a git log into one.
- Latest version first, with the release date; keep an `Unreleased` section at the top and move it into a
  new version section at release time.
- Group changes as Added (new features), Changed (existing functionality), Deprecated (soon to be removed),
  Removed, Fixed and Security.
- Mark a pulled release `[YANKED]` rather than hiding it.
- For an API, add per entry: the affected endpoints and fields, who must act and by when, and a link to a
  migration guide.

## Classify the change
GitHub's REST API page is a worked example. Breaking: removing an operation, removing or renaming a parameter or
response field, adding a new required parameter, making an optional parameter required, changing a type,
removing enum values, adding a validation rule to an existing parameter, changing authentication or
authorization requirements. Additive: adding an operation, optional parameter, optional request header, response
field, response header or enum value.

## Communicate
- GitHub releases breaking changes only in a new, date-named API version, gives advance notice, supports
  the previous version for at least 24 more months after a new one ships, and documents per version what broke
  and how to upgrade. Publish your own notice period; do not copy that figure unless you commit to it.
- Never edit history silently; correct with a new dated entry.

## Checked
Date: 2026-11-01. Confirmed on Keep a Changelog 1.1.0 (principles, ordering, Unreleased, change types, YANKED)
and GitHub REST breaking-changes page (lists, advance notice, 24 months, per-version upgrade notes). Removed:
tool names (oasdiff, buf), HTTP header names, 90-day email window and channel advice, example entry and
Stripe reference, which these pages do not state.
Method: documentation only; no commands were run.
