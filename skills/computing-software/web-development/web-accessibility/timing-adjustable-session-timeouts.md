---
id: computing-software.web-development.web-accessibility.timing-adjustable-session-timeouts
name: timing-adjustable-session-timeouts
category: computing-software
field: web-development
product: web-accessibility
tags: [enough-time, seizure-safety, timing-adjustable, session-timeout-warning, wcag-2-2-1, extend-session, timeouts-wcag-2-2-6, data-loss-prevention]
level: practitioner
status: verified
description: "Meeting WCAG 2.2.1 Timing Adjustable: session-timeout warnings that let users extend, accessible countdown dialogs, preserving data across re-login."
sources:
  - https://www.w3.org/WAI/WCAG22/Understanding/timing-adjustable.html
  - https://www.w3.org/WAI/WCAG22/Understanding/timeouts.html
  - https://design-system.service.gov.uk/patterns/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Timing adjustable and session timeouts

**Goal:** users who read, type or navigate slowly aren't logged out or timed out mid-task without warning and a way to get more time.

## 1. The rule (2.2.1, A)
For each time limit set by the content, at least one: user can **turn it off**, **adjust** it over a range at least ten times the default, or **extend** it - warned before time expires and given at least 20 seconds to extend with a simple action (e.g. press a key), at least ten times (WCAG 2.2 text). Exceptions: real-time events (auctions), essential limits (exams with rules), limits over 20 hours.

## 2. Session timeout warning pattern
- Warn ~2 minutes before (not 20 s - screen reader users need time to find and operate it).
- Modal dialog: "You'll be signed out in 2 minutes due to inactivity" with **Stay signed in** (primary, focused) and Sign out.
- Stay signed in -> call a keep-alive endpoint that extends the server session; close the dialog, return focus.
- Don't announce every second of a countdown: update visible text each second but announce via live region only at intervals (e.g. each minute) or not at all after the initial dialog announcement.
- Count "activity" server-side correctly: background polling shouldn't keep sessions alive forever, but user typing in a long form should (send a heartbeat on input every few minutes).

```js
const WARN_AT = SESSION_MS - 2 * 60_000;
let warnTimer = setTimeout(showWarning, WARN_AT);
async function staySignedIn() {
  await fetch('/session/keepalive', { method: 'POST', headers: { 'X-CSRF-Token': csrf } });
  clearTimeout(warnTimer); warnTimer = setTimeout(showWarning, WARN_AT); closeDialog();
}
```

## 3. If it does expire
Preserve entered data (2.2.5 AAA: re-authenticate without losing data): save drafts server-side or in storage, and after re-login return to the same step with fields restored. Tell users the time limit up front for flows that have one (2.2.6 AAA Timeouts).

## 4. Other time limits
Auto-dismissing toasts/notifications (keep important ones until dismissed), timed quizzes (offer extension), OTP code expiry (allow resend easily).

## Verify
- [ ] Warning dialog appears with enough time, is announced, and Stay signed in extends the server session.
- [ ] Expiry during a long form keeps the user's data after signing in again.
- [ ] Toasts with important info don't vanish before they can be read.
