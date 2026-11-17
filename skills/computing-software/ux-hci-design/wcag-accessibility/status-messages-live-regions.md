---
id: computing-software.ux-hci-design.wcag-accessibility.status-messages-live-regions
name: status-messages-live-regions
category: computing-software
field: ux-hci-design
product: wcag-accessibility
tags: [status-messages, aria-live]
level: practitioner
status: docs-checked
description: "Use role=status and role=alert or live regions so dynamic messages are announced without moving focus (SC 4.1.3)."
sources:
  - https://www.w3.org/WAI/WCAG22/Understanding/status-messages.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# 4.1.3 Status Messages (AA)
- A status message is a change in content that is not a change of context and that gives information on the success or results of an action, the waiting state of an application, the progress of a process, or the existence of errors. It must be programmatically determinable through role or properties so assistive technology can present it without receiving focus.
- Results and state: `role="status"` (technique ARIA22). Suggestions or error warnings: `role="alert"` or live regions (ARIA19). The page says an alert role is only necessary where no change of context takes place.
```html
<div role="status">5 results returned</div>
```
- Typical cases from the page: a search result count, "Added to cart" item counts, a "form was successfully submitted" message, and "5 errors on page".
- A dialog that takes focus is a change of context, not a status message.
- Live regions can make an application too "chatty" for screen reader users; the page advises user testing to get the right amount of feedback.

## Verify
- [ ] With a screen reader, trigger the action: the message is announced without focus moving.

## Checked

2026-11-09. Confirmed on the Understanding SC 4.1.3 page: the level, the status message definition, techniques ARIA22 and ARIA19, the example messages, the dialog exclusion and the chatty-region warning. Removed: the rule that the live region container must pre-exist in the DOM, the polite and assertive guidance, and the keystroke advice, none of which the page states.

Method: documentation only; no commands were run.
