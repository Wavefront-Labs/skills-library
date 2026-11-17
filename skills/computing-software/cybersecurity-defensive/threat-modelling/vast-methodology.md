---
id: computing-software.cybersecurity-defensive.threat-modelling.vast-methodology
name: vast-methodology
category: computing-software
field: cybersecurity-defensive
product: threat-modelling
tags: [vast-methodology, vast, process-flow-diagram, operational-threat-model, threatmodeler]
level: practitioner
status: docs-checked
description: "VAST (Visual, Agile and Simple Threat) modelling: separate application and operational threat models, built on ThreatModeler and aimed at large organisations."
sources: ["https://threatmodeler.com/threat-modeling-methodologies-vast/", "https://insights.sei.cmu.edu/blog/threat-modeling-12-available-methods/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# VAST threat modelling

VAST (Visual, Agile, and Simple Threat modelling) is based on ThreatModeler, an automated
threat-modelling platform. It is designed to be adopted by large organisations across their
whole infrastructure, and it works with common practices such as STRIDE.

## Two model types (SEI summary)
VAST recognises that development and infrastructure teams differ in operations and concerns,
so it requires two kinds of model:
- **Application threat models** use process-flow diagrams and represent the architectural
  point of view.
- **Operational threat models** are created from an attacker point of view, based on data-flow
  diagrams.
This split lets VAST fit into an organisation's development and DevOps lifecycles.

## Stated aims (ThreatModeler page)
- Scalable: enterprise-wide, automating processes and integrating with Agile environments.
- Automated: removes repetitive tasks, which the vendor says cuts threat evaluation from
  hours to minutes (a vendor claim, not independently measured).
- Integrated with Agile DevOps and tools used in software development.
- Collaborative: stakeholders with different skills evaluate threats and prioritise mitigation.
- Continuous, with consistent outcomes aligned with Agile workflows.

## When it fits
- Large estates that want consistent, repeatable output across many applications.
- Teams already using ThreatModeler; the VAST description is closely tied to that vendor's
  platform, so check that the concepts work without it before adopting the method on its own.
- SEI notes no single method is recommended over another; combine methods as needed and pick
  by risk, security or privacy focus, time, experience and stakeholder involvement.

## Verify
- [ ] Each application has an application model and, where it depends on shared
      infrastructure, a linked operational model.
- [ ] The team can say why VAST was chosen over STRIDE, PASTA or another method.

## Checked
Confirmed 2026-11-09 against the SEI blog "Threat Modeling: 12 Available Methods" (VAST section) and the ThreatModeler VAST page (both read in full).
Removed as unconfirmed: the founder attribution, the component-library workflow, "built by development teams / infrastructure teams" ownership, SDLC export steps, the roll-up between models, and the gotchas about library quality and PFDs missing back-end flows.
Method: docs-checked 2026-11-09 against insights.sei.cmu.edu threat-modeling-12-available-methods and threatmodeler.com threat-modeling-methodologies-vast
