---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.nalsd-requirements-quantification
name: nalsd-requirements-quantification
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [requirements-quantification, sla-to-qps, nalsd, back-of-the-envelope, system-design, capacity-estimation]
level: advanced
status: docs-checked
description: "Turn vague system requirements into numbers for NALSD: transaction rates, record sizes, daily data volume and SLOs as measurable targets, using the Workbook's AdWords example."
sources: ["https://sre.google/workbook/non-abstract-design/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Turning requirements into numbers (NALSD)

Workbook "Non-Abstract Large System Design": start with the problem statement, gather requirements, then iterate
through designs, turning the whiteboard design into concrete resource estimates at each step. Reasoning and stated
assumptions matter more than the final values.

## Questions to ask
- How many users / devices / events, and what transaction rates (the Workbook example assumes 500,000 search
  queries per second and 10,000 ad clicks per second)?
- What do they do and how often? Read/write ratio? Sizes of requests, responses, stored records?
- Which SLOs matter to the user? State each as a target and a percentage of requests or time.
- Retention: how long must data be kept? Growth?

## Conversion recipe
```
records/day     = rate_per_second * 86,400 seconds
storage/day     = records/day * bytes_per_record
```
Worked example (Workbook, AdWords click-through-rate dashboard): the query log is rounded up to 2 KB per entry
(aggressive rounding on purpose, to avoid hitting a limit unexpectedly), so
`(5 x 10^5 queries/s) x (8.64 x 10^4 s/day) x (2 x 10^3 bytes) = 86.4 TB/day`; the click log is about 2% of that
(10,000 clicks / 500,000 queries); with index overhead the Workbook rounds up to about 100 TB per day of logs.

## SLOs as numbers
The Workbook states the requirements as SLOs, so the design can be compared with an error budget:
- 99.9% of dashboard queries complete in under 1 second.
- 99.9% of the time, the CTR data displayed is less than 5 minutes old.

## Rules of thumb (from the chapter)
- Use scientific notation to limit errors from arithmetic on inconsistent units.
- Round up aggressively and write the assumption down; early assumptions heavily influence results.
- Write numbers where everyone can see them; every design iteration is checked against them.

## Gotchas
- Requirements without a stated percentile or window are not quantified.
- Mixing units (bits/bytes, per second/per day) is the usual source of order-of-magnitude errors.

## Verify
- [ ] Requirements table with transaction rates, record sizes, daily volume and measurable SLOs.
- [ ] Each number traces to a stated assumption.

## Checked
2026-11-01. Confirmed against the SRE Workbook chapter "Introducing Non-Abstract Large System Design" (sre.google/workbook/non-abstract-design): the AdWords example, 500,000 queries/s and 10,000 clicks/s, the two SLOs, 2 KB rounded entry size, 86.4 TB/day, the 2% click ratio, the use of scientific notation and aggressive rounding.
Removed: peak-factor and replication recipes with no page backing, the invented storage figures, generic latency/availability examples (43 min budget, 200 ms, 60 s freshness) and the classroom source.
Method: documentation only; no commands were run.
