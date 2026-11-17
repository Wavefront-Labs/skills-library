---
id: media-communication.technical-writing.ux-writing.microcopy-and-error-messages
name: microcopy-and-error-messages
category: media-communication
field: technical-writing
product: ux-writing
tags: [ux-writing, microcopy, content-design, product-copy, ui-text, error-messages, empty-states, button-labels, labels, form-copy, validation-messages, confirmation-dialogs, onboarding, tooltips, voice-and-tone, figma, string-management, localisation, accessibility, screen-readers, plain-language, content-testing]
level: practitioner
status: docs-checked
description: "Write error messages that are visible, plain, constructive and accessible: placement, tone, advice, timing, preserving input, and WCAG 3.3.1 and 3.3.3."
sources: ["https://www.nngroup.com/articles/error-message-guidelines/", "https://www.w3.org/WAI/WCAG22/Understanding/error-identification.html", "https://www.w3.org/WAI/WCAG22/Understanding/error-suggestion.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Microcopy and error messages

**Goal:** interface text that helps people act: honest errors with a way out, written
with design and engineering, not pasted in at the end.

## 1. Error messages: what happened, and what to do now
An error message is a system-generated interruption telling the user about an
incomplete, incompatible or undesirable situation. Nielsen's usability heuristic 9 is
"Help users recognize, diagnose, and recover from errors".
| Bad | Better |
|---|---|
| "Error 403" | "You don't have permission to edit this page. Ask the page owner for access." |
| "Invalid input" | "Enter a date in the format DD/MM/YYYY." |
| "Something went wrong" | "We couldn't save your changes because the connection dropped. Your draft is kept; try again." |

## 2. Visibility
- Show the message **close to the error's source**, next to the field that needs attention.
- Use noticeable, redundant indicators (bold, high-contrast text, highlighting of the
  affected element, an icon), but never colour or animation alone.
- Match the display to the impact: toasts, banners or conditional labels for issues
  needing little interaction; reserve modal dialogs for severe errors.
- **Timing:** do not show errors prematurely. Do not treat tabbing out of an empty
  field as an error. Inline, real-time feedback suits error-prone fields such as password
  requirements, where users are unlikely to get it right first time.

## 3. Communication
- Plain, human-readable language without jargon. Hide or minimise obscure error codes
  and abbreviations; show them for diagnostic purposes only.
- Describe the exact problem concisely ("An error occurred" has no context), without
  excess technical precision that clashes with the user's mental model.
- Offer constructive advice or a remedy (for example, when an item is out of stock, say
  when it returns or offer a restock notification).
- Positive tone; do not blame the user. Avoid words such as "invalid", "illegal" or
  "incorrect" that imply fault. Avoid humour: it goes stale when users see the error often.

## 4. Efficiency
- Safeguard against likely mistakes (such as a mention of an attachment with none attached);
  the worst error message is one that does not exist.
- **Preserve the user's input** so they can edit it instead of starting over.
- Reduce correction effort: where you can guess, offer a short list of fixes (for example
  a button for the city that matches the ZIP code entered).
- Briefly explain how the system works, linking to supporting material if needed (do not overdo it).
- Reserve novelty or humour for total-failure moments (such as overloaded servers) that
  are rare and offer no recourse.

## 5. Accessibility (WCAG 2.2)
- **3.3.1 Error Identification:** if an input error is automatically detected, the item
  in error is identified and the error is described to the user in text. Colour or other
  visual indicators may be used in addition, not instead.
- **3.3.3 Error Suggestion:** if an error is automatically detected and suggestions for
  correction are known, provide them, unless that would jeopardise the security or
  purpose of the content.

## Gotchas
- Generic "Something went wrong" covering several different failures; ask engineering to
  distinguish them.
- Errors shown in red alone, or after a form reloads with no hint that submission failed.

## Verify
- [ ] Every error message states what happened and what to do, without blame.
- [ ] Message sits next to the field in error and is not conveyed by colour alone.
- [ ] Errors are not shown before the user has had a chance to answer.
- [ ] User input is preserved after an error.
- [ ] Errors are identified in text (3.3.1) with correction suggestions where known (3.3.3).

## Checked
2026-11-09. Confirmed against the Nielsen Norman Group "Error-Message Guidelines" article (heuristic 9, placement, redundant indicators, severity and modal use, premature errors, plain language, codes, precise description, remedies, tone and the avoid-"invalid" wording, humour, safeguards, preserving input, fix lists, novelty only in total failure) and the WCAG 2.2 Understanding pages for 3.3.1 and 3.3.3 (wording of each criterion). Removed unconfirmed material: button and label rules, empty-state, translation and string-management advice, testing methods, and aria usage.
Method: documentation only; no commands were run.
