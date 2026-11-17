---
id: creative-arts.design-for-form-and-experience.ux-design.writing-helpful-error-messages
name: writing-helpful-error-messages
category: creative-arts
field: design-for-form-and-experience
product: ux-design
tags: [error-message-writing, error-messages, ux-writing, content-design, validation-messages, microcopy]
level: practitioner
status: docs-checked
description: "Write error messages that say what happened, why, and how to fix it, in plain words without blame, placed at the field and with a recovery path."
sources:
  - https://www.nngroup.com/articles/error-message-guidelines/
  - https://www.nngroup.com/articles/hostile-error-messages/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Writing error messages

**Goal:** the person knows what went wrong and can fix it in one step.

## Formula
1. **What happened** in plain words: "We couldn't save your changes."
2. **Why** if known and useful: "You're offline."
3. **What to do:** "Reconnect and try again. Your edits are kept on this device." Provide the action as a button (Retry).

## Rules
- Human language, never codes alone (put the code, such as ERR_504, in small text for support).
- **No blame:** "Enter a date as DD/MM/YYYY", not "You entered an invalid date".
- **Specific:** describe the issue concisely and precisely: "Password needs N or more characters" beats "Invalid password" or "An error occurred".
- **Position and proximity:** show the message close to the error's source; preserve what the user typed so they can edit it.
- **Not colour-only:** never use only colour or animation to mark an error; add text and an icon.
- **Tone:** positive; assist the user, do not admonish. Avoid humour, which goes stale when users meet the error often.

## Verify
- [ ] Each message has what, why (when known) and next step.
- [ ] Appears at the problem and keeps input.
- [ ] Reviewed for blame and jargon.

## Checked
2026-11-01. Confirmed against NN/g Error-Message Guidelines and Hostile Patterns in Error Messages: positive tone and no blame, concise precise wording, message near the source, preserve input, avoid humour, never colour or animation alone. Removed (not stated on those pages): ARIA attributes, login-message exception, all-caps/exclamation/Oops rule, form-level summary, tell-the-rule-first, Apple HIG and Material citations.
Method: documentation only; no commands were run.
