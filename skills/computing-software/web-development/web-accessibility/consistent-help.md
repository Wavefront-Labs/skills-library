---
id: computing-software.web-development.web-accessibility.consistent-help
name: consistent-help
category: computing-software
field: web-development
product: web-accessibility
tags: [readable, predictable, consistent-help, wcag-3-2-6, wcag-2-2, help-mechanisms, contact-details, chatbot-accessibility]
level: practitioner
status: docs-checked
description: "Meeting WCAG 2.2 SC 3.2.6 Consistent Help: placing contact details, help links, chat and self-help in the same relative order across pages."
sources:
  - https://www.w3.org/WAI/WCAG22/Understanding/consistent-help.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Consistent help (WCAG 3.2.6)

**Goal:** people who get stuck can always find help in the same place (new A criterion in WCAG 2.2, aimed at cognitive disabilities).

## 1. The rule
If a web page contains any of these help mechanisms, and they're repeated on multiple pages, they occur in the **same order relative to other page content** on each page (unless the user changes it):
- Human contact details (phone, email, hours)
- Human contact mechanism (chat with a person, contact form, social media messaging)
- Self-help option (FAQ, help centre, support page link)
- Fully automated contact mechanism (chatbot)

It doesn't require providing help - only consistency where it exists.

## 2. Implementation
- Put help in a shared layout region: e.g. a "Help" link in the header utility nav and the same contact block in the footer of every page, including checkout and account flows.
- The criterion compares order relative to other page content (as the page is serialized); a floating chat launcher should therefore sit at the same place in the page order on every page, and not be hidden on some steps and moved on others.
- On multi-step forms, a consistent "Get help with this form" link near the top of each step.
- Responsive layouts may move help (header -> menu on mobile); the SC notes that visual position is likely to be consistent for the same page variation, such as a CSS breakpoint.

## 3. Make help usable too
- Chatbots: keyboard accessible, labelled launcher, live-region announcements of replies, a way to reach a human.
- Contact details as text (selectable, `tel:`/`mailto:` links), not images.

## Verify
- [ ] On each template (home, listing, product, checkout steps, account), help appears in the same relative location.
- [ ] Chat launcher reachable by keyboard and named.
- [ ] Help present in error/timeout pages too.

## Checked

2026-10-26, against WCAG 2.2 normative text and Understanding documents (w3c/wcag repository, checked 2026-10-26). Confirmed from the normative text of 3.2.6 Consistent Help (Level A, new in WCAG 2.2): the four help mechanism types (human contact details, human contact mechanism, self-help option, fully automated contact mechanism), same order relative to other page content, user-initiated changes excepted, and page variation by breakpoint. The Understanding page confirms the examples (FAQ, chat client, chatbot).

Method: documentation only; no commands were run.
