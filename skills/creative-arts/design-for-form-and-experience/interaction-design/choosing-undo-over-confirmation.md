---
id: creative-arts.design-for-form-and-experience.interaction-design.choosing-undo-over-confirmation
name: choosing-undo-over-confirmation
category: creative-arts
field: design-for-form-and-experience
product: interaction-design
tags: [undo, confirmation-dialog, destructive-actions, reversible-actions, soft-delete, error-prevention, confirm-vs-undo]
level: practitioner
status: draft
description: "Choose undo or confirmation: make actions reversible with undo toasts and soft delete, and reserve specific, well-written confirmations for irreversible or high-cost operations."
sources:
  - "Aza Raskin, A List Apart - Never Use a Warning When you Mean Undo (alistapart.com/article/neveruseawarning)"
  - "Nielsen Norman Group - Confirmation Dialogs Can Prevent User Errors (If Not Overused) (nngroup.com/articles/confirmation-dialog)"
  - "Don Norman, The Design of Everyday Things (2013), error chapter"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Undo over confirmation

**Goal:** protect users from mistakes without training them to click through warnings.

## Why not confirm everything
Confirmation dialogs get dismissed by habit (the "are you sure" reflex), slow frequent tasks, and still fail when the user is on autopilot. **Undo** works for slips because it does not interrupt the flow.

## Decision rule
1. **Reversible and frequent** (archive, delete an email, remove an item from a list, move): act immediately, show **undo** (toast, 5-10 s, see `creative-arts.design-for-form-and-experience.interaction-design.designing-toasts-and-snackbars`), plus a trash or archive with recovery window (soft delete 30 days).
2. **Irreversible or costly** (permanent delete, send payment, publish to everyone, delete an account, bulk actions on many items, revoke access): confirm.
3. **Edit-undo** within editors: multi-level Ctrl/Cmd+Z, redo, history.
4. Technically hard undo? Consider a **delay-send** window or a pending state before commit.

## Writing a good confirmation
- Title states the consequence: "Delete 3 projects permanently?"
- Body names what is lost and whether it can be recovered; includes counts and names.
- Buttons use verbs: **Delete 3 projects** and **Cancel**; the destructive button is not the default focus; no "OK/Yes".
- For very high cost add typed confirmation (type the project name) or a short cooldown.
- Do not stack confirmations or confirm on non-destructive navigation.

## Gotchas
- Undo must really restore state (server-side too); test failure cases.
- Announce undo availability to screen readers and keep it reachable by keyboard.

## Verify
- [ ] Every destructive action is classified reversible or irreversible.
- [ ] Reversible ones use undo or soft delete, irreversible ones confirm with specific text.
