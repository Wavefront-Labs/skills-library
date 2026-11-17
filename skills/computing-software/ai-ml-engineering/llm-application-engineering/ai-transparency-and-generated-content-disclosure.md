---
id: computing-software.ai-ml-engineering.llm-application-engineering.ai-transparency-and-generated-content-disclosure
name: ai-transparency-and-generated-content-disclosure
category: computing-software
field: ai-ml-engineering
product: llm-application-engineering
tags: [llm-application, ai-transparency, content-provenance, c2pa, eu-ai-act, disclosure]
level: practitioner
status: docs-checked
description: "Meet AI transparency duties: tell users they are dealing with AI, mark synthetic media with C2PA or watermarks, label deepfakes and published AI text, and document limitations."
sources:
  - https://artificialintelligenceact.eu/article/50/
  - https://c2pa.org/specifications/specifications/2.1/index.html
  - https://deepmind.google/models/synthid/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Transparency and AI-generated content disclosure

**Goal:** people know when they are interacting with AI or seeing AI-generated content, generated media carries machine-readable provenance, and the product meets applicable legal duties.

## EU AI Act Article 50 (applies from August 2026)
- **Providers of AI systems interacting with people** (chatbots, voice agents) must design them so people are informed they are interacting with AI, unless obvious from context.
- **Providers of generative AI** (text, image, audio, video) must mark outputs in a machine-readable format and make them detectable as artificially generated, as far as technically feasible.
- **Deployers** of emotion recognition or biometric categorisation must inform the people exposed.
- **Deployers** generating deepfakes must disclose that content is artificially generated or manipulated; AI-generated text published to inform the public on matters of public interest must be disclosed unless it underwent human editorial review with editorial responsibility.
Disclosure must be clear and given at the latest at first interaction or exposure. Other jurisdictions (for example US state laws on AI disclosure and bot use) add their own rules - check where you operate.

## Implementation
- **Conversational UI:** persistent label ("AI assistant") plus first-message disclosure; voice agents state it at call start; never instruct the model to claim to be human.
- **Media provenance:** attach C2PA Content Credentials (the C2PA specifications cover certifying the source and history of media); use invisible watermarking where available (e.g. SynthID, which embeds watermarks in AI-generated images, audio, text and video). Check that provenance survives your delivery pipeline.
- **Text:** label AI-drafted content in publishing workflows; record human review for the editorial exemption.
- **Documentation:** user-facing description of what the AI does, its limitations and how to reach a human; model/system cards for business customers.

## Beyond compliance
Log which outputs were AI-generated, with model version, so you can answer questions later.

## Verify
- [ ] Every AI interaction surface discloses AI involvement at first contact.
- [ ] Generated images/audio/video carry C2PA manifests (checked with a verifier) after the full delivery pipeline.
- [ ] Legal review recorded for each jurisdiction served.

## Checked
2026-11-01. Confirmed against the Article 50 text (artificialintelligenceact.eu): application from 2 August 2026, paragraphs 1-5 duties, first-interaction timing, editorial-review exemption; C2PA specifications index; SynthID page. Removed: manifest field names, metadata-stripping claim, NIST AI 600-1 sentence (PDF not readable).
Method: documentation only; no commands were run.
