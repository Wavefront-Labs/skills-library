---
id: computing-software.software-engineering.code-review.reviewing-documentation-changes
name: reviewing-documentation-changes
category: computing-software
field: software-engineering
product: code-review
tags: [code-review, docs-review, technical-writing, docs-as-code, style-guide, documentation]
level: practitioner
status: draft
description: "Review documentation changes: accuracy against the code, audience and task focus, runnable examples, structure and style guide, links, and docs updated alongside code."
sources: ["https://developers.google.com/style", "https://diataxis.fr/", "https://www.writethedocs.org/guide/docs-as-code/", "https://vale.sh/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Reviewing documentation changes

## Accuracy (most important)
- Do the steps work? Run the commands/code samples, or check CI that tests docs examples
  (doctest, `mdx` snippet tests, `pytest --doctest-glob`, `cargo test` for Rust doc examples).
- Do versions, flags, defaults and screenshots match the current code?
- When code changes behaviour, the same PR updates docs (README, reference, changelog, comments).
  Removed features are removed from docs.

## Audience and type (Diataxis)
Is this a **tutorial** (learning by doing), **how-to** (solve a specific task), **reference**
(precise facts), or **explanation** (understanding)? Mixed types confuse: a reference page that
wanders into tutorial prose, or a how-to without the prerequisites.

## Clarity checks
- Title says what the page helps you do; first paragraph says who it's for and the outcome.
- Prerequisites listed up front; steps numbered, one action each; expected result after key steps.
- Concrete examples, copy-pasteable code blocks with language tags; placeholders clearly marked
  (`<PROJECT_ID>`) and explained.
- Short sentences, active voice, second person ("Run the command"), consistent terminology with the
  product UI and glossary (Google developer documentation style guide, Microsoft style guide).
- No "simply", "just", "easy". Avoid unexplained acronyms.
- Warnings/notes used sparingly and for real risks (data loss, security).

## Mechanics
- Links work and point to stable URLs (link checkers: lychee, markdown-link-check).
- Headings hierarchical, alt text on images, tables readable on mobile.
- Prose linting with Vale (style rules), markdownlint for formatting, spell check with a project
  dictionary.
- Rendered preview: review the built page (preview deployments), not only raw Markdown.

## Comment style
Suggest replacement wording with suggestion blocks; separate factual errors (blocking) from style
preferences (nits). Ask a domain expert to check technical claims you can't verify.
