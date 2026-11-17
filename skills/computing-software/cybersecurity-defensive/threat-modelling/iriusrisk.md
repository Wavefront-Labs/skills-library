---
id: computing-software.cybersecurity-defensive.threat-modelling.iriusrisk
name: iriusrisk
category: computing-software
field: cybersecurity-defensive
product: threat-modelling
tags: [iriusrisk, threat-modelling-tool, automated-threat-modelling, countermeasures, jira-integration]
level: practitioner
status: draft
description: "Model a system in IriusRisk: components and trust zones, questionnaires, rule-generated threats and countermeasures, risk states, and syncing countermeasures to Jira."
sources: ["https://support.iriusrisk.com/", "https://www.iriusrisk.com/threat-modeling-platform"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# IriusRisk threat modelling

IriusRisk is a commercial threat modelling platform (a free Community Edition exists with limits). Its core is
a **rules engine plus component library**: you draw components inside trust zones and the tool generates
threats and countermeasures from risk pattern libraries (STRIDE, CAPEC, OWASP, cloud-provider libraries)
mapped to standards such as ASVS, NIST 800-53 and PCI DSS.

## Workflow
1. **Create a project** from a template or blank; choose the libraries relevant to the stack.
2. **Diagram**: drag components (e.g. "AWS Lambda", "Web Service", "MySQL") into **trust zones** (Internet,
   Public Cloud, Internal). Dataflows between components can carry tags such as sensitive data. Trust zone
   ratings influence generated risk.
3. **Questionnaires** at project and component level refine the model ("Does the API use OAuth?"). Answers
   fire rules that add or remove threats and countermeasures.
4. **Threats view**: each threat shows inherent, current and projected risk. Mark threats Not Applicable
   with a justification rather than deleting them.
5. **Countermeasures view**: states include Required, Recommended, Implemented, Rejected and Not Applicable.
   Implemented lowers current risk; Rejected leaves residual risk that a named owner must accept.
6. **Issue tracker integration**: push Required countermeasures to Jira or Azure DevOps; status syncs back so
   closing the ticket marks the countermeasure Implemented.
7. **Test status**: countermeasures can carry test results so "implemented" claims are evidenced.

## Automation
- Import from Terraform/CloudFormation or draw.io/Visio diagrams to bootstrap the model; always review
  imported trust zones.
- The REST API lets CI create or update projects and pull risk summaries for release gates.

## Gotchas
- Generated threat lists are long; budget triage time and tune libraries rather than bulk-marking N/A.
- The model is only as current as the diagram; tie updates to architecture change reviews.
- Risk numbers are relative within the tool, not calibrated probabilities.

## Verify
Every Required countermeasure has an issue link or an accepted-risk owner, and the project's current risk is
within the release gate threshold.
