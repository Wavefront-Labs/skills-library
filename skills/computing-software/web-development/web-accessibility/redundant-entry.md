---
id: computing-software.web-development.web-accessibility.redundant-entry
name: redundant-entry
category: computing-software
field: web-development
product: web-accessibility
tags: [input-assistance, accessible-forms, redundant-entry, wcag-3-3-7, wcag-2-2, autofill-previous-answers, same-as-billing, cognitive-accessibility]
level: practitioner
status: docs-checked
description: "Meeting WCAG 2.2 SC 3.3.7 Redundant Entry: auto-populating or offering previously entered information within a process instead of asking again."
sources:
  - https://www.w3.org/WAI/WCAG22/Understanding/redundant-entry.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Redundant entry (WCAG 3.3.7)

**Goal:** within one process, users never have to type the same information twice (new A criterion in WCAG 2.2; helps cognitive and motor disabilities).

## 1. The rule
Information previously entered by or provided to the user that must be entered again **in the same process** is either auto-populated or available to select. Exceptions: re-entry is essential (memory game), required to ensure the security of the content (the Understanding page gives preventing a password string from being displayed as an example), or the earlier info is no longer valid.

## 2. Patterns
- Billing address: a "Same as delivery address" checkbox that populates the fields (the Understanding page gives this exact example), editable afterwards.
- Multi-step forms: carry name/email forward; show them pre-filled rather than asking again on a later step.
- After validation errors: re-render with all values kept (server-side forms often drop them - including file inputs, where you should keep the uploaded file reference).
- Back button: returning to a step shows previous answers (store in session/state, not just the DOM).
- Select from earlier: "Use the email you entered: alex@… " or a list of previously entered addresses/contacts.

## 3. Implementation notes
- Keep process state server-side (session) or in client state that survives back/forward (`sessionStorage`, history state); don't rely on the browser restoring form fields.
- Don't block paste anywhere (paste is how many users avoid retyping).
- `autocomplete` tokens (1.3.5) help across sessions but don't satisfy 3.3.7 alone - it's about data within the process.

## Verify
- [ ] Walk each multi-step flow: no field asks for data already given earlier in the flow.
- [ ] Submitting with an error keeps every other value.
- [ ] Browser Back to a previous step shows prior answers.

## Checked

2026-10-26, against WCAG 2.2 normative text and Understanding documents (w3c/wcag repository, checked 2026-10-26). Confirmed from the normative text of 3.3.7 Redundant Entry (Level A, new in WCAG 2.2): auto-populated or available to select, with the exceptions essential, security and no longer valid; the Understanding page names memory games and the same-as-shipping checkbox. Removed the unconfirmed password-confirmation commentary and the checked-by-default detail.

Method: documentation only; no commands were run.
