---
id: computing-software.it-support-helpdesk.user-support-communication.ai-drafted-knowledge-articles
name: ai-drafted-knowledge-articles
category: computing-software
field: it-support-helpdesk
product: user-support-communication
tags: [it-support-helpdesk, user-support-communication, ai-knowledge-drafting, knowledge-base, ai-in-support, kcs, generative-ai]
level: practitioner
status: draft
description: "Use AI to draft knowledge base articles from resolved tickets: input selection, templates, redaction, technical review, KCS states, labelling, and keeping AI drafts accurate."
sources:
  - https://library.serviceinnovation.org/KCS/KCS_v6/KCS_v6_Practices_Guide
  - https://www.servicenow.com/docs/bundle/xanadu-it-service-management/page/product/now-assist-itsm/concept/now-assist-itsm-kb-generation.html
  - https://www.nist.gov/itl/ai-risk-management-framework
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# AI-drafted knowledge articles

Generative AI can turn a resolved incident's notes into a first-draft article in seconds (ServiceNow Now Assist KB generation, Zendesk/Freshservice AI, Copilot). A human still owns accuracy.

## Inputs that produce good drafts
- Tickets with clear resolution notes: symptom, environment, cause, steps that fixed it (see resolution notes that feed knowledge).
- Several similar resolved tickets for the same issue, so the draft generalises.
- Your KB **template** in the prompt: Title (symptom in user words), Applies to, Symptoms, Cause, Resolution steps, Verification, Related articles.

## Redact
Strip names, emails, device names, IPs, internal URLs not meant for the audience, and any credentials before generating, especially for end-user-facing articles.

## Review checklist (before publish)
1. Every step reproduced or confirmed by the technician who fixed it; commands and menu paths checked against vendor docs.
2. No invented settings, registry keys or cmdlets.
3. Audience correct: end-user article has no admin-only steps; internal article flags risk (registry, admin rights).
4. Title and keywords match how users describe the problem (searchability).
5. Duplicate check: update an existing article instead of creating another.

## Workflow (KCS-aligned)
- AI draft enters as **Work in Progress / Draft**; reviewer edits; publish as **Not Validated** (internal) then **Validated** after reuse confirms it works.
- Mark articles "AI-assisted, reviewed by <name>" if your policy requires disclosure.
- Track article reuse and "did this help" feedback; retire articles with low accuracy ratings.

## Gotchas
- AI smooths over uncertainty: a one-off workaround becomes "the fix". Keep cause statements tentative unless confirmed.
- Drafts from bad notes produce confident nonsense; improve note quality first.

## Verify
A second technician follows the published article on a test device and resolves the issue without extra steps.
