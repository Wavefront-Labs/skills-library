---
id: computing-software.ai-ml-engineering.llm-application-engineering.data-poisoning-and-llm-supply-chain
name: data-poisoning-and-llm-supply-chain
category: computing-software
field: ai-ml-engineering
product: llm-application-engineering
tags: [llm-application, data-poisoning, llm-supply-chain, owasp-llm-top-10, model-provenance, safetensors]
level: practitioner
status: docs-checked
description: "Defend against OWASP LLM03/LLM04: vetted suppliers, pickle risks and model scanning, signing and file hashes, SBOM/AI-BOM, data provenance and versioning, poisoning monitoring."
sources:
  - https://genai.owasp.org/llmrisk/llm032025-supply-chain/
  - https://genai.owasp.org/llmrisk/llm042025-data-and-model-poisoning/
  - https://huggingface.co/docs/hub/security-pickle
  - https://github.com/protectai/modelscan
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Data / model poisoning and LLM supply chain

**Goal:** models, adapters, datasets and documents entering your LLM system come from trusted sources, are verifiable, and cannot silently plant backdoors or false knowledge.

## Supply chain (LLM03)
- **Suppliers:** vet data sources and suppliers, including terms and privacy policies; review them regularly for changes in security posture or terms.
- **Model files:** pickle is the default format for PyTorch weights and loading a pickle file can run arbitrary code. Hugging Face suggests loading models only from users and organizations you trust, relying on signed commits, and notes safetensors as a simple weights format it is working on. ModelScan (Protect AI) scans H5, Pickle and SavedModel files for unsafe code. Hub pickle-import scanning is not foolproof; verification is your responsibility.
- **Integrity and provenance:** OWASP advises using only models from verifiable sources, with third-party integrity checks using signing and file hashes, and code signing for externally supplied code.
- **Evaluate third-party models:** apply AI red teaming and evaluations when selecting one; OWASP warns models can be fine-tuned to pass published benchmarks while carrying targeted triggers.
- **Components:** apply vulnerability scanning, management and patching (OWASP A06:2021 Vulnerable and Outdated Components); keep a patching policy and rely on maintained versions of APIs and underlying models.
- **Inventory:** keep a signed SBOM; OWASP says AI BOMs and ML SBOMs are an emerging area and suggests starting with OWASP CycloneDX. Use BOMs for licence inventories and audits too.
- **Collaborative development environments:** monitor and audit for abuse.

## Poisoning (LLM04)
- Track data origins and transformations (OWASP CycloneDX or ML-BOM) and verify data legitimacy at every model development stage.
- Vet data vendors; validate model outputs against trusted sources to detect signs of poisoning.
- Sandbox the model's exposure to unverified data sources and put infrastructure controls so it cannot reach unintended data; use anomaly detection to filter adversarial data.
- Use data version control (DVC) to track dataset changes and detect manipulation.
- Use specific datasets for fine-tuning per use case.
- Store user-supplied information in a vector database so it can be adjusted without retraining.
- Test robustness with red team campaigns and adversarial techniques; monitor training loss and model behaviour with thresholds for anomalous outputs.
- At inference, RAG and grounding can reduce hallucination risk.

## Verify
- [ ] Every production model has a recorded source, integrity check (signature or file hash) and approval.
- [ ] No pickle-format third-party weights loaded without scanning and a trusted source.
- [ ] Fine-tuning datasets have tracked provenance and versions.

## Checked
2026-11-01. Confirmed against OWASP LLM03:2025 Supply Chain, OWASP LLM04:2025 Data and Model Poisoning, Hugging Face "Pickle Scanning" docs and the ModelScan README. Removed: torch.load weights_only, from_pretrained revision pinning, picklescan, OpenSSF/Sigstore signing, typosquatting and download-history advice, LoRA-specific advice, user-feedback and RAG-corpus tables, and the detection section, none of which the cited pages state.
Method: documentation only; no commands were run.
