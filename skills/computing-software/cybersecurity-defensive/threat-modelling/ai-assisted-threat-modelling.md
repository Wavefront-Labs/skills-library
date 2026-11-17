---
id: computing-software.cybersecurity-defensive.threat-modelling.ai-assisted-threat-modelling
name: ai-assisted-threat-modelling
category: computing-software
field: cybersecurity-defensive
product: threat-modelling
tags: [ai-assisted-threat-modelling, llm, threat-modelling, stride-gpt, dread, attack-trees]
level: practitioner
status: docs-checked
description: "Use STRIDE GPT to draft STRIDE threat models, attack trees, DREAD scores and test cases from an application description, then verify the output by hand."
sources: ["https://raw.githubusercontent.com/mrwadams/stride-gpt/master/README.md", "https://www.threatmodelingmanifesto.org/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AI-assisted threat modelling with STRIDE GPT

STRIDE GPT is an open-source tool that uses LLMs to generate threat models and attack trees
for an application, based on the STRIDE methodology. The user provides application details
such as the application type, authentication methods, and whether it is internet-facing or
processes sensitive data, and the model generates its output from them.

## What the tool does (README)
- Interfaces: a CLI with an interactive REPL (`pip install stride-gpt`), and a Streamlit web
  interface that is also available as a Docker image.
- CLI commands: `/analyze` is an agentic codebase analysis (planner, per-subsystem agents,
  cross-cutting synthesis); `/quick` makes a single-shot threat model from a written
  application description.
- Outputs: STRIDE threat models, attack trees, suggested mitigations, DREAD risk scoring, and
  Gherkin test cases; formats are Markdown, JSON, SARIF and a self-contained HTML view.
- Inputs besides text: architecture diagrams (image upload or an embedded draw.io editor whose
  XML is parsed for components, connections and trust boundaries) and GitHub repository
  analysis. Data flow diagrams can be generated, edited as Mermaid source and fed back in as
  the system model.
- Threats can carry MITRE ATT&CK and ATLAS technique IDs. The README says reference cards
  instruct the agent to use only catalogued IDs and names, to avoid hallucinated IDs, and that
  the cards are regenerated from upstream data rather than written from model recall.
- Reference cards also cover OWASP LLM Top 10 and OWASP Top 10 for Agentic Applications for
  GenAI and agentic applications.
- The README states application details are not stored by the tool, and that it supports many
  model providers through LiteLLM, including local hosting with LM Studio.
- From version 0.20 each reported threat carries code evidence that is checked against the
  file on disk, and each subsystem records why its analysis stopped, so a failed subsystem is
  distinguishable from one that found nothing.

## Using it responsibly
- The Threat Modeling Manifesto's four questions still apply; "Did we do a good enough job?"
  remains a human judgement.
- The Manifesto's anti-pattern "Hero Threat Modeler" and its pattern "Varied Viewpoints"
  support having a team review generated output rather than one person accepting it.
- Treat generated technique IDs and mitigations as claims to check against the real system
  and the real catalogue.

## Verify
- [ ] Each generated threat refers to a component that exists in the design.
- [ ] Any ATT&CK, ATLAS or OWASP identifier resolves to the entry it names.

## Checked
Confirmed 2026-11-09 against the STRIDE GPT README (features and changelog, first 150 lines read, including versions 0.12 to 0.21) and the Threat Modeling Manifesto page.
Removed as unconfirmed: the recommended workflow of structured prompt tables, stripping secrets and using no-training enterprise endpoints, the claim that models skew to web threats, the prompt injection and false completeness risks as stated, provenance marking, and the OWASP LLM Top 10 page as a source, which was not read.
Method: docs-checked 2026-11-09 against the mrwadams/stride-gpt README on raw.githubusercontent.com and threatmodelingmanifesto.org
