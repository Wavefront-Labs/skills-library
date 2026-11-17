---
id: computing-software.devops-ci-cd.semaphore-ui.session-lifetime
name: session-lifetime
category: computing-software
field: devops-ci-cd
product: semaphore-ui
tags: [session, session-timeout, auth, cookie, security, semaphore-ui]
level: practitioner
status: docs-checked
description: "Limit Semaphore sessions with auth.session_inactivity_hours and auth.max_session_life_hours."
sources:
  - https://semaphoreui.com/docs/admin-guide/authentication/local
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Session lifetime limits

Goal: end sessions on a schedule that fits your security policy.

Two independent limits apply; whichever hits first signs the user out.

Inactivity timeout, counted from the last request (every authenticated request, including background polling by an open tab, resets it). Default 168 hours (seven days):

```json
{ "auth": { "session_inactivity_hours": 8 } }
```

Absolute limit, counted from sign-in so even an active session ends. Default `0` means no absolute limit:

```json
{ "auth": { "max_session_life_hours": 12 } }
```

Combine them:

```json
{ "auth": { "session_inactivity_hours": 8, "max_session_life_hours": 12 } }
```

Why both: a browser left open on a page that polls the API keeps the inactivity timer alive, so only the absolute limit reliably ends such a session. Use it on shared workstations or where compliance demands periodic re-authentication.

## Checked

2026-11-07. Read in full: the Local accounts page, from its markdown source in the semaphore-docs repository (admin-guide/authentication/local.md; no snippet files included). Confirmed: the two independent limits, the request-based inactivity timer including background polling, the 168 hour default, the absolute limit and its default of 0, the three config examples, and the reason both are needed. Removed: the secure-cookie gotcha and the wait-past-the-limit Verify step, neither stated on the page.
Method: documentation only; no commands were run.
