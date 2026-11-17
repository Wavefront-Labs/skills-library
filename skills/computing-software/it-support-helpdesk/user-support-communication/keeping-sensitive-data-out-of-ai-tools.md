---
id: computing-software.it-support-helpdesk.user-support-communication.keeping-sensitive-data-out-of-ai-tools
name: keeping-sensitive-data-out-of-ai-tools
category: computing-software
field: it-support-helpdesk
product: user-support-communication
tags: [it-support-helpdesk, user-support-communication, ai-in-support, ai-data-privacy, generative-ai, approved-ai-tools, data-classification, prompt-redaction, enterprise-data-protection, comptia-a-plus, ai-acceptable-use]
level: intro
status: draft
description: "Use generative AI in support without leaking data: approved vs public tools, what never goes into prompts, redacting logs, and answering users about AI."
sources:
  - "https://www.comptia.org/certifications/a"
  - "https://www.nist.gov/itl/ai-risk-management-framework"
  - "https://learn.microsoft.com/en-us/copilot/microsoft-365/enterprise-data-protection"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# keeping-sensitive-data-out-of-ai-tools

Goal: get the productivity of AI assistants without pasting customer data,
credentials or internal secrets into a service that may retain or train on
them (A+ 220-1202 4.10 AI — appropriate use, data privacy).

## Know which tools are approved
- **Enterprise tools** under a company agreement (e.g. Microsoft 365
  Copilot / Copilot Chat with enterprise data protection, signed in with
  the work account; other vendors' enterprise tiers) — prompts not used for
  training, covered by data processing terms.
- **Public/consumer AI** (personal accounts, free web chatbots, browser
  extensions) — treat anything typed as published. Many organisations
  block or restrict them.
Check the AI acceptable-use policy; if none exists, assume public tools
are not approved for work data.

## Never paste
Passwords, keys, tokens, connection strings; customer or employee personal
data; full logs with usernames/IPs/hostnames of sensitive systems;
proprietary code or documents marked confidential; security incident
details.

## Redact before asking
Replace identifying values with placeholders: `user@contoso.com` →
`<user>`, server names → `<server-a>`, IPs → `10.x.x.x`. Ask about the
pattern ("Event 4771 failure code 0x18 from a DC — what does it mean?"),
not the specific person.

## Users asking the desk
- "Can I use ChatGPT for this report?" → point to the policy and the
  approved tool; explain the risk in one line.
- Browser extensions claiming AI features often read every page — handle as
  unapproved software.
- Report suspected data leakage to an AI tool to security, like any data
  incident.

## Gotchas
- "It's a private chat" is not a contract — only enterprise terms are.
- Uploading files (spreadsheets, PDFs) to AI tools carries the same risk as
  pasting text.
- AI-generated content may need marking per policy.

## Verify
You can name your organisation's approved AI tool and policy; sample
tickets/prompts in enterprise tools show placeholders, not raw sensitive
values.
