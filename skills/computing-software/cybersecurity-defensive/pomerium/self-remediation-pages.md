---
id: computing-software.cybersecurity-defensive.pomerium.self-remediation-pages
name: self-remediation-pages
category: computing-software
field: cybersecurity-defensive
product: pomerium
tags: [self-remediation, error-details, policy-explanation, custom-denial-page, branding-header]
level: intro
status: docs-checked
description: "Show users why Pomerium Enterprise denied access and how to fix it using Error Details, per-policy Explanation and Remediation, and a custom header."
sources:
  - https://raw.githubusercontent.com/pomerium/documentation/main/content/docs/capabilities/self-remediation.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Enterprise feature that replaces a generic denial with guidance.

Setup:
1. Per route: open the **General** tab and turn on **Error Details**. If off, users see only a generic 403.
2. Per policy: fill **Explanation** (short reason, e.g. outdated browser) and **Remediation** (steps, e.g. download the latest update). If either is blank the page shows the **Policy ID** instead.
3. Optional global **custom header** in Branding settings, shown on every denial page. It supports basic Markdown for help desk links, disclaimers or images.

Example workflow: a critical exploit hits an old browser; security updates the policy to deny unpatched browsers; the explanation names the missing patch and the remediation links the software portal; users update, refresh and regain access without a ticket.

Benefits stated: faster self-service fixes, enforceable patching, fewer help desk requests, clearer messaging.

Pair with white-labeling (branding) for a fully branded interface.

## Checked

2026-11-04. Confirmed against the Self-Remediation page: Enterprise feature, Error Details toggle on route General tab, generic 403 when off, Explanation and Remediation fields, Policy ID fallback, global Branding header with Markdown, example workflow, benefits. Removed a closing caution the page does not state.

Method: documentation only; no commands were run.
