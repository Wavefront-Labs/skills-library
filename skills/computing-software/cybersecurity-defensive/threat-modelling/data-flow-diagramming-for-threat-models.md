---
id: computing-software.cybersecurity-defensive.threat-modelling.data-flow-diagramming-for-threat-models
name: data-flow-diagramming-for-threat-models
category: computing-software
field: cybersecurity-defensive
product: threat-modelling
tags: [data-flow-diagram, dfd, trust-boundary, threat-modelling, decomposition, external-entity, process, data-store, security-review]
level: practitioner
status: docs-checked
description: "Draw the data flow diagram a threat model needs: the five things to show, high-level plus detail views, brainstorming as an alternative, and review questions."
sources: ["https://cheatsheetseries.owasp.org/cheatsheets/Threat_Modeling_Cheat_Sheet.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Data flow diagramming for threat models

**Goal:** a system model that answers "what are we working on?" well enough that threat identification
(STRIDE or another technique) finds the threats that matter. Source: OWASP Threat Modeling Cheat Sheet.

## What the cheat sheet says
- System modelling is the foundation: without understanding the system you cannot tell which threats apply most.
- Data flow diagrams (DFDs) are arguably the most common approach. They visually model a system, its data
  flows and its interactions with external entities.
- Whatever technique you use, the model must give a clear view of **trust boundaries, data flows, data stores,
  processes and external entities**. These often represent possible attack points.
- Create DFDs with a diagramming tool or whiteboard and save them in a form the team can update.
- For complex systems, use a high-level overview alongside more detailed diagrams of individual components.
- Brainstorming is an alternative or complement: it engages all participants, builds shared terminology and
  quickly surfaces key processes and dependencies, and suits sessions with less technical participants. Combine
  its results with formal modelling for a better understanding of the domain.

## Cloud systems
Traditional techniques such as STRIDE or DFDs often need adaptation for cloud architectures. Account for
cloud components (virtual networks, IAM roles, managed services, storage buckets), shared responsibility
(which controls the provider manages), dynamic environments (containers, serverless, ephemeral
infrastructure) and compliance and data residency.

## Practice notes
- Label each data flow with what it carries and mark trust boundaries wherever trust changes, then apply the
  threat prompts to components, flows and boundaries.
- Validate the diagram with the people who built the system.

## Verify (the cheat sheet's review questions)
- [ ] Does the DFD (or comparable model) accurately reflect the system?
- [ ] Have all threats been identified, and does each have an agreed response?
- [ ] Is the model formally documented and stored where those with need to know can access it?
- [ ] Reviewed by all stakeholders, not just development or security teams.

## Checked
2026-11-01. Confirmed against the OWASP Threat Modeling Cheat Sheet: system modelling purpose, DFDs, the five elements to show, update-friendly storage, overview plus detail diagrams, brainstorming, cloud adaptation and review questions.
Removed: element shapes and per-element common mistakes, Level 0/1/2 decomposition guidance, update triggers, direction-of-arrow advice, and tool claims (Microsoft Threat Modeling Tool, Threat Dragon), because the page read does not state them.
Method: documentation only; no commands were run.

Related: computing-software.cybersecurity-defensive.threat-modelling.stride-threat-modelling,
computing-software.cybersecurity-defensive.threat-modelling.attack-trees-and-pasta
