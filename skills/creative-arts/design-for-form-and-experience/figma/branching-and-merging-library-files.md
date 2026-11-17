---
id: creative-arts.design-for-form-and-experience.figma.branching-and-merging-library-files
name: branching-and-merging-library-files
category: creative-arts
field: design-for-form-and-experience
product: figma
tags: [figma-branching, branching, merge, library-contribution, review-changes, figma-libraries, figma]
level: practitioner
status: draft
description: "Use Figma branching to change a library safely: create a branch, edit, request review, resolve conflicts and merge into main, then publish."
sources:
  - "Figma Help Center - Branching and merging (help.figma.com/hc/en-us/articles/360063144053)"
  - "Figma Help Center - Create and merge branches (help.figma.com)"
  - "Figma Help Center - Branching availability: Organization and Enterprise plans (help.figma.com)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Branching and merging

**Availability:** branching is for **Organization and Enterprise** plans; the main file must be editable by you (branch creators need edit access).

## Workflow
1. In the main library file, open the **file name menu > Create branch**; name it by purpose (`button-loading-state`). A branch is a copy you can edit without affecting main or consumers.
2. **Edit** components, styles and variables in the branch; use sticky notes and comments for context; keep scope small (one change set).
3. **Request review:** from the branch toolbar, **Open for review** and assign reviewers; reviewers see a **visual diff** (before/after thumbnails for changed components, styles, variables) and can **approve** or request changes in comments.
4. **Update from main** if main changed meanwhile (to pull the changes into the branch).
5. **Merge** into main: the **Review changes** screen shows the diff; resolve **conflicts** (the same component changed in both) by choosing the branch or main version per item; confirm merge.
6. **Publish** the library from main to deliver the changes (`creative-arts.design-for-form-and-experience.figma.publishing-and-updating-a-figma-library`); optionally archive the merged branch.

## Practices
- Keep branches short-lived (days) to limit conflicts; one branch per feature or fix.
- Use branches for all risky changes (restructuring variants, renaming properties); review the diff carefully before merging, and publish only after review.
- Define contribution rules (who may merge, required reviewers) and align with the contribution model (`creative-arts.design-for-form-and-experience.design-systems.running-a-design-system-contribution-model-and-team`).
- Link branch to the code PR or ticket in the description.

## Gotchas
- Branching works best with the **library file** as a single source; avoid editing the same component in several branches.
- Merging does not publish; consumers update only after publish.
- Deleting a branch removes unmerged work (version history may help).

## Verify
- [ ] Branch named for one purpose, reviewed with a diff, conflicts resolved explicitly.
- [ ] Merge followed by a deliberate publish with release notes.
