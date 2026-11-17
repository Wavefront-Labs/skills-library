---
id: creative-arts.design-for-form-and-experience.interaction-design.designing-error-recovery-states
name: designing-error-recovery-states
category: creative-arts
field: design-for-form-and-experience
product: interaction-design
tags: [error-recovery, error-states, ui-states, retry, graceful-degradation, 404-pages, error-pages]
level: practitioner
status: draft
description: "Design error states that let users recover: classify the failure, say what happened, preserve work, offer retry and alternatives, and design 404, 500 and permission pages."
sources:
  - "Nielsen Norman Group - Error Message Guidelines and Visibility of System Status (nngroup.com/articles/error-message-guidelines)"
  - "web.dev - The Offline Cookbook (web.dev/articles/offline-cookbook)"
  - "GOV.UK Design System - Problem with the service pages (design-system.service.gov.uk/patterns/problem-with-the-service-pages)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Error recovery states

**Goal:** when something fails, nothing is lost and the next step is obvious.

## Classify
- **User-fixable** (validation, permission, wrong credentials): tell them exactly what to change.
- **Transient system** (timeout, network, 5xx): retry, with automatic backoff where safe.
- **Permanent** (not found, removed, forbidden): explain and redirect.
- **Partial failure:** some items failed; show which, retry only those.

## Principles
1. **Preserve user work:** keep typed data, drafts and selections; autosave locally before submit.
2. **Say what happened** in plain language, and what was not affected ("Your payment was not taken.").
3. **Offer actions** in order: Retry (primary), alternative path (use another method, go back, contact support), and a reference or incident ID for support.
4. **Place the error where the failure is:** inline for a field or card, full-page for a failed route, banner for global problems.
5. **Prevent loops:** after repeated failures, change the suggestion (check status page, contact).
6. **Status information:** link to the status page for outages; show last successful update time for stale data.

## Pages
- **404:** friendly, with search, popular links and the home link; log broken inbound links.
- **500/503:** apology plus time estimate if known, kept very light (cache-served static page), not an exposed stack trace.
- **403/permission:** explain whose permission is needed and how to request it.
- **Offline:** see `creative-arts.design-for-form-and-experience.interaction-design.designing-offline-and-degraded-states`.

## Verify
- [ ] Each failure class has a designed state with a recovery action.
- [ ] No data loss on error; support ID shown.
- [ ] Errors are announced to assistive tech and use plain language.
