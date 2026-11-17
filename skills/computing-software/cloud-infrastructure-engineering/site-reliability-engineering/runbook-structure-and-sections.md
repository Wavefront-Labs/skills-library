---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.runbook-structure-and-sections
name: runbook-structure-and-sections
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [runbook-structure, runbook-sections, runbooks, playbooks, alert-runbook, runbook-template]
level: practitioner
status: docs-checked
description: "Structure an alert playbook entry so on-call can act fast: severity, impact, debugging suggestions, mitigation actions, with a minimal agreed set of fields."
sources: ["https://sre.google/workbook/on-call/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Runbook structure and sections

SRE playbooks give high-level instructions on how to respond to automated alerts. Per the SRE Workbook they explain the severity and impact of the alert and include debugging suggestions and possible actions to mitigate impact and fully resolve it. In SRE, whenever an alert is created, a corresponding playbook entry is usually created, and these guides reduce stress, mean time to repair (MTTR) and the risk of human error.

## Template (one entry per alert)
```markdown
# <AlertName>
Severity / impact: what users experience and how serious it is.
Debugging suggestions: links to the monitoring console, what to check first, recent changes.
Mitigation: actions to reduce impact (rollback, drain, disable a feature).
Resolution: what fully resolves it.
Escalation: who to ask for help.
```
The field names are a suggestion; the Workbook only names severity, impact, debugging suggestions and mitigation/resolution actions. Agree on your own minimal structure.

## Rules
- Every alert gets a corresponding playbook entry, and a proposed alert is reviewed with that entry.
- Pages should link to the relevant monitoring consoles, and playbooks should carry advice for each type of alert.
- The Workbook's mitigation guidance for entries: roll back a recent change if safe, disable a feature via a feature flag, or drain requests away from the elements showing the bug.
- Decide with the team what minimal, structured details playbooks must have, and notice when entries accumulate much information beyond those details; turn hard-won production knowledge into automation or monitoring consoles.
- Teams differ: some keep entries general so they change slowly (one entry for all "RPC Errors High" alerts, read with an architecture diagram), others write step-by-step entries to reduce variability and MTTR. Pick one stance so entries are not pulled in different directions.
- If an entry is a deterministic list of commands run every time the alert fires, implement automation instead.

## Verify
- [ ] Every paging alert has a playbook entry that the page links to.

## Checked
Method: docs-checked 2026-11-09 against the SRE Workbook chapter "On-Call" (playbooks and their maintenance, identification and mitigation delay techniques, alerting). The SRE Book "Being On-Call" page was read and does not mention playbooks, and the Prometheus Operator runbooks site was not read, so both were dropped. Removed the "roughly triples MTTR" figure, the PromQL and kubectl command examples, `runbook_url` annotation advice and the last-verified field, none of which were confirmed on the pages read.
