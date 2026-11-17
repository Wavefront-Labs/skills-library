---
id: computing-software.digital-forensics-incident-response.incident-response-process.attribution-confidence-and-estimative-language
name: attribution-confidence-and-estimative-language
category: computing-software
field: digital-forensics-incident-response
product: incident-response-process
tags: [estimative-language, threat-intelligence, attribution, incident-report, dfir]
level: advanced
status: docs-checked
description: "Express attribution and analytic confidence correctly: ICD 203 likelihood terms and percentage ranges, confidence kept separate, fact versus judgement, avoiding over-attribution."
sources: ["https://archive.dni.gov/files/documents/ICD/ICD-203.pdf", "https://www.cia.gov/resources/csi/static/Words-of-Estimative-Probability.pdf", "https://attack.mitre.org/groups/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Attribution confidence and estimative language

**Goal:** executives, insurers and law enforcement read attribution statements literally.
Use calibrated language so "likely" means the same thing every time.

## Probability terms (ICD 203 scale)
ICD 203 requires one set of terms for likelihood, each tied to a range. Do not mix terms from
different rows; if you must, add a disclaimer that they express the same probability.

| Term (alternative wording) | Probability |
|---|---|
| almost no chance (remote) | 1-5% |
| very unlikely (highly improbable) | 5-20% |
| unlikely (improbable) | 20-45% |
| roughly even chance (roughly even odds) | 45-55% |
| likely (probable) | 55-80% |
| very likely (highly probable) | 80-95% |
| almost certain (nearly certain) | 95-99% |

**Confidence** is a separate statement about the basis of the judgement: ICD 203 ties it to the
logic and evidence behind it, including the quantity and quality of source material and the
analyst's understanding of the topic. Likelihood refers to an event or development.
ICD 203 says a product that uses a confidence level (for example "high confidence") must not
combine it with a likelihood term in the same sentence. Write two sentences: "The activity is
likely linked to group X. We have moderate confidence in this judgement because ..."

## Evidence for attribution, weakest to strongest (practitioner judgement, not from the sources)
- Single shared IOC (IP, domain): weak.
- Commodity tools (Cobalt Strike, Mimikatz): little attribution value.
- Custom malware family with code overlap: moderate.
- Consistent TTPs, infrastructure patterns, victimology and timing across multiple incidents: stronger.
- Law-enforcement or provider attribution with access you lack: cite it, do not repeat it as your own.

## Writing it
- Separate underlying information ("the loader matched family X by YARA rule Y") from
  judgements ("we assess..."). ICD 203 asks for this distinction and for stating key assumptions.
- State alternatives considered (copycat, false flag, shared tooling).
- Note that threat-group names are activity clusters: the MITRE ATT&CK Groups page says
  organisations' definitions may partially overlap or disagree, and its "Associated Groups" are
  best-effort name overlaps, not exact matches.

## Gotchas
- "Nation-state" claims based on sophistication alone.
- Attribution rarely changes response actions; do not delay containment for it.
- Involve legal before an attribution statement leaves the team.

## Verify
Every attribution sentence has a probability term from one ICD 203 row, a stated confidence in a
separate sentence, and cited evidence.

## Checked
Date: 2026-11-08. Confirmed from ICD 203 (text extracted from the PDF): the seven likelihood terms and
percentage ranges, the no-mixing rule, confidence tied to evidence quality, and the ban on combining
confidence and likelihood in one sentence; from the MITRE ATT&CK Groups page: overlap and Associated
Groups wording. The CIA Words of Estimative Probability paper was read (it uses a different, older
scale) and is context only. Removed as unsourced: the "moderate confidence ... likely" example
sentence, ransomware affiliate-brand claim, and sanctions and war-exclusion claim. The evidence ladder
is labelled as judgement.
Method: documentation only; no commands were run.
