---
id: computing-software.software-engineering.code-review.suggested-changes-github-gitlab
name: suggested-changes-github-gitlab
category: computing-software
field: software-engineering
product: code-review
tags: [code-review, suggested-changes, github, gitlab, suggestion-blocks, batch-suggestions]
level: intro
status: draft
description: "Use suggested changes in GitHub and GitLab reviews: suggestion block syntax, multi-line suggestions, batching commits, and when a suggestion is better than a comment."
sources: ["https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/reviewing-changes-in-pull-requests/commenting-on-a-pull-request", "https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/reviewing-changes-in-pull-requests/incorporating-feedback-in-your-pull-request", "https://docs.gitlab.com/user/project/merge_requests/reviews/suggestions/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Suggested changes in GitHub and GitLab

## Syntax
Select the line(s) in the diff, comment, and use a fenced block named `suggestion`; its content
replaces the selected lines exactly:
````
```suggestion
    if not order.items:
        raise EmptyOrderError(order.id)
```
````
- GitHub: click the "Insert a suggestion" (+/-) button, or drag across line numbers for a
  multi-line suggestion. An empty suggestion block deletes the lines.
- GitLab: same `suggestion` block; multi-line with offsets, e.g. `suggestion:-2+1` covers 2 lines
  above and 1 below the commented line.

## Applying
- Author clicks **Commit suggestion** (GitHub) / **Apply suggestion** (GitLab).
- **Batch**: GitHub "Add suggestion to batch" then "Commit suggestions" makes one commit for many;
  GitLab "Add suggestion to batch" likewise. Avoids a commit per typo.
- Authors with write access (or the PR author on forks with "allow edits by maintainers") can apply.
- Applied suggestions still need CI to pass; suggestions don't run tests.

## When to use
- Small, concrete fixes: typos, naming, a missing null check, a simpler expression, doc wording.
- When explaining in words would take longer than showing the code.
- Not for large redesigns: describe the approach instead; long suggestions are hard to read and
  apply cleanly.
- Not for code you haven't checked compiles: a broken suggestion wastes a CI cycle. Prefix with
  "untested:" if unsure.

## Etiquette
Combine a suggestion with the reason ("`Path.read_text` closes the file for us"), mark optional
ones as such, and let the author decide whether to apply or adapt.
