---
id: computing-software.general-digital-literacy.office-suites.collaborative-editing-and-comments
name: collaborative-editing-and-comments
category: computing-software
field: general-digital-literacy
product: office-suites
tags: [office-suites, collaborative-editing, real-time-editing, comments, mentions, merge-conflicts, offline-editing, co-authoring, google-docs-comments, word-comments, concurrent-editing]
level: intro
status: docs-checked
description: "Co-edit a document live with others without stepping on each other's changes: comments, @-mentions, resolving conflicts, and editing offline safely."
sources:
  - https://support.google.com/docs/answer/65129
  - https://support.google.com/docs/answer/6033474
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Collaborative editing and comments — several people, one document, no mess

**Goal:** edit a shared document, sheet or deck alongside other people without
overwriting each other's work, communicate through comments rather than scattered
side-channel messages, and avoid conflicting copies from offline edits. Steps below are
for Google Docs; other suites (Word, LibreOffice) have equivalents in their own help.

## 1. Comments and mentions (Google Docs)
- Select text, an image or cells, click the **Add comment** icon in the toolbar, type
  and click Comment. Feedback attached to a spot keeps its context.
- **@-mention** a person in a comment (type `@` and a name or email, then pick the
  suggestion): they get an email notification. If they lack access to the file, share it
  with them first.
- To **assign an action item**, put `@` or `+` before the assignee's email, tick
  "Assign to" and click Assign. The assignee is emailed; the Done button in the
  comment's top-right corner closes it.
- **Resolve** a comment instead of deleting it. To find a closed comment, click Comments
  at the top of the window, then Re-open.

## 2. Suggesting vs. direct editing
- When reviewing someone else's document, use **Suggesting** mode: switch the mode at the
  top right from Editing to Suggesting. Changes then show as suggestions for the owner
  to accept or reject instead of silently altering the text.
- Accept or reject a suggestion by choosing its comment and clicking Accept or Reject.
  For a whole round, Tools › Review suggested edits, then Accept all or Reject all.

## 3. Avoiding conflicts in practice
- Agree who edits which **section** of a long document before a big simultaneous
  session, especially in spreadsheets.
- If a file was edited offline or as a local copy, your sync service may create a
  separate conflict copy when it reconnects (see organising-files-and-folders). Compare
  the two files, merge by hand, then delete the duplicate. Check for conflict copies
  right after reconnecting rather than continuing to edit blind.

## Verify
- [ ] The file lives on a service that supports shared editing, if that's the intent.
- [ ] Feedback on someone else's document used Suggesting mode (or your suite's
      equivalent), not direct edits.
- [ ] Comments were resolved, not deleted, once addressed.
- [ ] After offline editing, you checked for a conflict-copy file before assuming the
      merge went cleanly.

## Checked
2026-11-01. Confirmed from Google Docs Help on comments (add, @-mention, assign, resolve,
re-open) and on Suggesting mode (switching mode, accept/reject, Accept all). Removed:
Microsoft 365 co-authoring and Track Changes claims, keyboard shortcuts, presence-icon
location, the character-level merge and "first keystroke wins" claims, and the merge
conflict notification claim, which these pages do not state.
Method: documentation only; no commands were run.
