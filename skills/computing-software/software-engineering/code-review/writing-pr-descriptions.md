---
id: computing-software.software-engineering.code-review.writing-pr-descriptions
name: writing-pr-descriptions
category: computing-software
field: software-engineering
product: code-review
tags: [code-review, pr-author, change-author, pr-description, cl-description, pull-request-template, reviewer-context]
level: practitioner
status: docs-checked
description: "Write pull request / CL descriptions that let reviewers and future readers understand what changed and why: first line, context, testing, risk and rollout."
sources: ["https://google.github.io/eng-practices/review/developer/cl-descriptions.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Writing PR descriptions

**Goal:** a reviewer understands the change before reading the diff, and a future developer
searching history understands what was done and why. Google's guide calls the description a
public record of change that becomes a permanent part of version control history.

## What a description must say
- **What** change is being made, summarised so readers need not read the whole change.
- **Why**: the context you had as the author, including decisions not reflected in the source.
  Code shows what the software does but not why it exists, so a future developer may not know
  whether it is safe to move "Chesterton's fence".

## First line
- A short summary of specifically what the change does, followed by a blank line.
- A complete sentence written as an order (imperative): "Delete the FizzBuzz RPC and replace it
  with the new system." rather than "Deleting the FizzBuzz RPC and replacing it with the new
  system."
- It appears in history summaries, so it must stand alone and let a searcher tell what the
  change did and how it differs from others.

## Body
The rest fills in details: a brief description of the problem and why this is the best approach,
shortcomings of the approach, and where relevant bug numbers, benchmark results and links to
design documents. Links may not be visible to future readers because of access restrictions or
retention policies, so include enough context in the text itself. Even small changes deserve
some context.

## Bad descriptions (all from the guide)
"Fix bug", "Fix build.", "Add patch.", "Moving code from A to B.", "Phase 1.", "Add convenience
functions.", "kill weird URLs." Short, but they say neither what nor why.

## Good shapes
- **Functionality change:** first words say what the change does; the rest covers the problem,
  why this solution, and implementation notes.
- **Refactoring:** first line says what the change does and how it differs from before; the
  body covers implementation, context, that the solution is not ideal, and future direction.
- **Small change needing context:** first sentence says what is done; the rest explains why.

## Tags
Optional manual labels such as `[tag]`, `#tag` or `tag:`. Keep them short in the first line,
since too many or too long tags overwhelm it; move them into the body if needed.

## Generated and evolving changes
Descriptions of tool-generated changes should follow the same advice. Changes can alter a lot
during review, so re-read the description before submitting to check it still matches.

## Checked

2026-11-08. Read in full: Google eng-practices "Writing good CL descriptions". Confirmed: what and why, first-line rules, imperative example, body contents, bad-description list, the three good-description shapes, tags guidance and re-checking before submit. Removed: the invented example body with incident, rps, flag and timing figures, the squash-merge and template advice, and the GitHub pull request template source.

Method: documentation only; no commands were run.
