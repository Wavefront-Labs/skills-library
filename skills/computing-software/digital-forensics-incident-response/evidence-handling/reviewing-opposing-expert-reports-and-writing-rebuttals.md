---
id: computing-software.digital-forensics-incident-response.evidence-handling.reviewing-opposing-expert-reports-and-writing-rebuttals
name: reviewing-opposing-expert-reports-and-writing-rebuttals
category: computing-software
field: digital-forensics-incident-response
product: evidence-handling
tags: [rebuttal-report, expert-witness, peer-review, forensic-reporting, dfir]
level: advanced
status: draft
description: "Review an opposing forensic expert's report and write a rebuttal: reproduce their findings, test methods and assumptions, find omissions, and respond point by point without advocacy."
sources: ["https://www.law.cornell.edu/rules/frcp/rule_26", "https://www.law.cornell.edu/rules/fre/rule_702", "https://www.swgde.org/documents/published-complete-listing"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Reviewing opposing expert reports and writing rebuttals

Under FRCP 26(a)(2)(D)(ii), rebuttal evidence is "intended solely to contradict or rebut evidence on the same subject matter" identified by the other side. A good rebuttal tests the other expert's work technically; it does not attack the person.

## Review method
1. **Inventory**: list each opinion and the facts it rests on; note the materials they had and did not have.
2. **Reproduce**: obtain the same evidence (or their images, with hashes) and repeat their key steps with the same and with independent tools. Record where results match and differ.
3. **Test assumptions**: time zones and clock offsets, which timestamp was used (e.g. NTFS `$SI` vs `$FN`, LNK target vs LNK file times), whether an artefact proves user action or only system activity, default tool settings that hide data.
4. **Check tool behaviour**: known bugs or parsing limits for the version they used; whether their tool was validated.
5. **Look for omissions**: exculpatory artefacts not mentioned, alternative explanations (malware, other users, sync clients, AV scans touching files), data sources not examined.
6. **Check logic**: does the conclusion follow from the facts, or does it leap from "file accessed" to "file stolen"?

## Writing the rebuttal
- Mirror their structure: quote or cite each opinion (by paragraph number), then your response, then the evidence.
- Categorise: agree; agree with qualification; disagree with reason; cannot assess (missing data).
- Concede what is correct; credibility comes from fairness.
- Include your reproduction method so the court can see why results differ.
- Keep to rebuttal scope; new affirmative opinions may be struck.

## Language
"The report states that the folder was opened by the user on 4 May. The shellbag entry cited records a last-write time of the BagMRU key, which updates when any child entry changes; it does not by itself establish when that folder was opened (Exhibit R-4)." Factual, sourced, no adjectives.

## Gotchas
- Courts expect experts to be independent (CPR Part 35 makes the duty to the court explicit); a rebuttal that reads like advocacy damages you.
- Errors you find in your own earlier work while reviewing must be disclosed and corrected.

## Verify
Every disagreement in the rebuttal cites a reproducible test or evidence item, and every opinion in the opposing report is addressed or explicitly left unaddressed with a reason.
