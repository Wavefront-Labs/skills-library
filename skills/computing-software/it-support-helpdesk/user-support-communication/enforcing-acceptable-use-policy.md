---
id: computing-software.it-support-helpdesk.user-support-communication.enforcing-acceptable-use-policy
name: enforcing-acceptable-use-policy
category: computing-software
field: it-support-helpdesk
product: user-support-communication
tags: [it-support-helpdesk, user-support-communication, privacy, acceptable-use-policy, aup-enforcement, shadow-it, policy-exception, personal-use, unapproved-software, comptia-a-plus]
level: practitioner
status: draft
description: "Apply the acceptable use policy at the desk: refusing out-of-policy requests well, the exception process, shadow IT, and when to escalate to security or HR."
sources:
  - "https://www.comptia.org/certifications/a"
  - "https://www.sans.org/information-security-policy/"
  - "https://www.ncsc.gov.uk/collection/device-security-guidance"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# enforcing-acceptable-use-policy

Goal: the desk applies policy consistently and politely, routes exceptions
properly, and doesn't become the morality police.

## Know the policy you're applying
AUP and related policies (BYOD, software installation, data handling,
remote access) define what users may do with company systems. Agents should
know where they're published and the handful of rules that generate
tickets: personal software installs, personal cloud storage, USB storage,
personal email forwarding, admin rights, browser extensions.

## Out-of-policy requests
1. Explain the rule briefly and neutrally — "Company laptops can't run
   personal VPN apps" — with the reason in one line (security, licensing,
   data protection).
2. Offer the **approved alternative** (company VPN, OneDrive instead of
   personal Dropbox, the licensed tool).
3. Offer the **exception process** (request with business justification,
   manager + security/app owner approval, time-bound) — and log it in the
   ticket.
4. Don't make exceptions yourself "just this once" — inconsistent
   enforcement is unfair and an audit finding.

## Shadow IT found during support
User relies on an unapproved SaaS/app: don't rip it out mid-ticket. Log it,
inform the user it needs review, raise to the app/security owner. The
business need is real; route it to procurement/architecture.

## When it's more than a request
Escalate (don't confront) when you see: deliberate security bypass
(disabling AV, tunnelling tools), data exfiltration signs (mass copying to
USB/personal cloud before notice period), harassment content, illegal
content (see prohibited content procedure). Report to security/HR per
process; keep ticket notes factual.

## Users signing the AUP
Onboarding: AUP acknowledgement captured (HR system or login banner);
helpdesk often fields "what does this mean" — answer with the policy text,
not personal interpretation.

## Verify
Exceptions are all ticketed with approval and expiry; similar requests get
the same answer across agents (QA sampling).
