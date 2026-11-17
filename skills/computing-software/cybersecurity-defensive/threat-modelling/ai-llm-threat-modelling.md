---
id: computing-software.cybersecurity-defensive.threat-modelling.ai-llm-threat-modelling
name: ai-llm-threat-modelling
category: computing-software
field: cybersecurity-defensive
product: threat-modelling
tags: [threat-modelling, ai-threat-modelling, llm-security, prompt-injection, nist-ai-100-2, rag-security]
level: advanced
status: docs-checked
description: "Threat model GenAI systems with the NIST AI 100-2e2025 taxonomy: direct and indirect prompt injection, RAG poisoning, supply chain, agents, mitigations."
sources: ["https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-2e2025.pdf"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AI/LLM system threat modelling

Source: NIST AI 100-2e2025, Adversarial Machine Learning: A Taxonomy and Terminology of
Attacks and Mitigations (March 2025). Use its GenAI taxonomy as the threat prompt list.

## Taxonomy for GenAI (violation, then attacks)
- Availability violations: data poisoning, indirect prompt injection, prompt injection.
- Integrity violations: data poisoning, indirect prompt injection, prompt injection, backdoor
  poisoning, targeted poisoning, misaligned outputs.
- Privacy compromises: indirect prompt injection, prompt injection, backdoor poisoning,
  membership inference, prompt extraction, leaking information from user interactions, training
  data attacks, data extraction, compromising connected resources.
- Misuse violations, and supply chain attacks (model poisoning).

## System elements to draw
Per the report: agents (software that iteratively prompts a model, calls functions with the
model's output and feeds results back; may have web browsing, code interpreters, memory and
planning), retrieval-augmented generation (RAG) sources, third-party models, plugins and
datasets, and the training pipeline (pre-training, instruction tuning, RLHF).

## Threats
- **Indirect prompt injection.** GenAI models combine the data and instruction channels, so an
  attacker who controls a resource the system uses (RAG source, web page, email) can inject
  instructions without interacting with the application. It is mounted by a third party and
  often harms the primary user. Demonstrated techniques include time-consuming background
  tasks, disabling capabilities, summary manipulation, knowledge base poisoning, hidden or
  multi-stage injections, self-propagating injections in email, forwarding private emails, and
  exfiltrating data by querying an attacker-controlled URL or through markdown image rendering.
- **Direct prompting attacks.** The attacker is the user; goals include enabling misuse
  (jailbreaks) and invading privacy (extracting the system prompt).
- **Data poisoning.** Large scraped datasets are an attack surface (for example attackers
  buying expired domains that serve dataset URLs). It can insert backdoors or change behaviour
  for trigger phrases, and can affect instruction tuning and RLHF.
- **Model supply chain.** Third parties may offer maliciously designed pre-trained models;
  backdoors can persist through fine-tuning or additional safety training. AI adds
  dependencies on data, third-party models and plugins.
- **Agents.** Tool use turns injection into hijacking: arbitrary code execution or
  exfiltration from the agent's environment.

## Mitigations named in the report
- Verify web downloads of training data with published cryptographic hashes; filter data
  (detecting poisoned samples is very difficult).
- Treat models as untrusted system components and design applications so risks from
  attacker-controlled output are reduced.
- Against indirect injection: task-specific fine-tuning, training for hierarchical trust in
  prompts, detection schemes, filtering instructions from third-party data, spotlighting
  prompts to separate trusted and untrusted data, and telling models to disregard
  instructions in untrusted data.
- Current mitigations do not fully protect, so assume injection is possible when a model sees
  untrusted input: use multiple LLMs with different permissions, or let models reach untrusted
  sources only through well-defined interfaces.
- Combine existing software supply chain risk management with provenance information for AI
  artefacts; vulnerability scanning of model artefacts helps only partly.

## Verify
- [ ] Every source of content that enters the model context is marked trusted or untrusted.
- [ ] Each agent tool has a stated permission and an assumption that injection is possible.

## Checked
Confirmed 2026-11-09 against NIST AI 100-2e2025 (pdftotext): taxonomy index, sections 3.2 supply chain, 3.4 indirect prompt injection and mitigations, and 3.5 agents.
Removed as unconfirmed: OWASP LLM Top 10 category mapping, MITRE ATLAS, specific controls (per-user ACL filtering of retrieval, safetensors, output encoding, rate limits, logging), the human-confirmation advice, the CI red-team verification, and the OWASP and MITRE sources, which were not read.
Method: docs-checked 2026-11-09 against NIST AI 100-2e2025 PDF via pdftotext
