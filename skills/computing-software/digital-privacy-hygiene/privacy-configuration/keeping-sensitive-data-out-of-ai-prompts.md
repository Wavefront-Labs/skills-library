---
id: computing-software.digital-privacy-hygiene.privacy-configuration.keeping-sensitive-data-out-of-ai-prompts
name: keeping-sensitive-data-out-of-ai-prompts
category: computing-software
field: digital-privacy-hygiene
product: privacy-configuration
tags: [digital-privacy-hygiene, privacy-configuration, ai-prompt-data-hygiene, ai-privacy, redaction, pii, health-data, third-party-data, browser-ai-extensions, local-llm]
level: intro
status: docs-checked
description: "Decide what never goes into a cloud AI prompt (IDs, health, others' data, secrets), redact documents before upload, and use local models for sensitive drafting."
sources:
  - "https://www.privacyguides.org/en/ai-chat/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Keeping sensitive data out of AI prompts

**Goal:** treat a cloud chatbot like an email to a company: it may be stored or breached.

## Why (Privacy Guides, "AI Chat")
Cloud-based AI software often collects your inputs, so your chats are not private from the provider; this creates
a risk of data breaches, and there is a real possibility an LLM leaks your private chat information in future
conversations with other users. Training data scraped from the web can include names and addresses. The page's
alternatives: refuse AI, use truly open-source models that publish their training data (it names OLMoE from Ai2),
or run models locally so your data never leaves your device.

## Practical rules (this skill's own guidance, not from the cited page)
## Never paste
- Passwords, API keys, recovery codes, seed phrases.
- Government ID numbers, full card/bank numbers.
- Other people's personal data (clients, patients, children) without their consent and,
  at work, without policy approval.
- Detailed health, legal or immigration specifics tied to your name, unless you accept the
  retention terms.

## Redact before uploading documents
- Replace names with roles ("Tenant A"), remove addresses, account numbers, dates of birth.
- Strip metadata from files (document properties, tracked changes) first (see
  `computing-software.digital-privacy-hygiene.privacy-configuration.metadata-scrubbing-photos-and-documents`).
- Screenshots: crop out notifications, tabs, email addresses.

## Safer options for sensitive work
- **Local models** for drafting with private material. Privacy Guides: you need a model and a client (it lists
  Kobold.cpp, Ollama and Llamafile); smaller models can run on as little as 8 GB of RAM at lower speeds, and its
  table gives 8 GB RAM for 7B, 16 GB for 13B and 72 GB with a GPU for 70B quantized models. Download models from the
  client's own library or from Hugging Face and verify the checksum.
- Check each cloud tool's temporary-chat and training opt-out settings.
- At work, use plans whose contract states retention and training terms.

## Watch for
- **Browser AI extensions** and "AI summariser" tools that read every page you visit.
- AI features in email/office suites that send document content to cloud models; check
  the admin or privacy settings.

## Verify
- [ ] Personal rule list written (what never goes in prompts) and shared with family/team.

## Checked
Checked 2026-11-08 against the full text of the Privacy Guides "AI Chat" page. The EFF SSD AI-tools URL returned 404
and was removed from sources. The sourced claims are the cloud-collection, breach and leakage risks and the local-model
alternative, hardware and download-verification details. The never-paste list, redaction steps and extension warning are
judgement guidance and are labelled as such; Ollama is confirmed on the page, LM Studio is not and was removed.
Method: documentation only; no commands were run.
