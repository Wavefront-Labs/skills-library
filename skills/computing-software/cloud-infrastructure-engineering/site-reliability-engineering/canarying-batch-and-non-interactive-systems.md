---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.canarying-batch-and-non-interactive-systems
name: canarying-batch-and-non-interactive-systems
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [canary-batch-systems, non-interactive-canary, canarying, data-pipelines, shadow-runs, release-engineering]
level: advanced
status: docs-checked
description: "Canary systems without request/response pairs (pipelines, batch work) per the SRE Workbook: size the canary to a work unit, keep workers in one pool, dry-run output, compare."
sources: ["https://sre.google/workbook/canarying-releases/", "https://sre.google/workbook/data-processing/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Canarying non-interactive and batch systems

The SRE Workbook "Canarying Releases" chapter focuses on interactive request/response systems, then lists the different considerations for asynchronous processing pipelines and says the general concept and high-level principles still apply.

## Considerations (Canarying Releases)
- **Duration depends on work-unit time.** Interactive canaries assume a work unit takes no more than a few seconds. Rendering pipelines or video encoding can take much longer, so make the canary duration at minimum span a single work unit.
- **Isolation is harder.** Many pipelines have a single work assigner and a fleet of workers, and in multistage pipelines a unit returns to the pool for the next stage. Make sure the workers processing a particular unit always come from the same pool, either canary or control; otherwise signals get mixed.
- **Metric selection is harder.** Consider end-to-end time to process a work unit (similar to latency in interactive systems) and the quality of the processing, which is application-specific.

## Considerations (Data Processing Pipelines)
- A canary is tied to the entire pipeline, not one process. You can process the same real production data as the live pipeline but skip writes to production storage; two-phase mutation can help.
- You often have to wait for the complete cycle of processing to finish before customer-impacting issues show up. After the dry run, compare canary results with the live pipeline for health and data differences.
- Per-task or per-region progression is not always possible. Pipelines using replicated data (Dataproc and Dataflow are named) have regional endpoints and cannot reload one cell in isolation; roll out to a small percentage of data first, or in dry-run mode.
- Verify with the same metrics used to track SLOs; the Workbook says this verification lends itself to automation.
- Canarying is an A/B comparison and both sides can change in tandem, so also use absolute measures such as defined SLOs.

## Checked
- 2026-11-08: the three non-interactive considerations were confirmed in "Canarying in Noninteractive Systems" on the Canarying Releases page; the pipeline points on the Data Processing Pipelines page ("Canarying"); the A/B caveat on the Canarying Releases page.
- Removed: the table of canary units per system type, the SQL diff example, the gating thresholds and the "reversible data" advice, none of which the pages state.
Method: docs-only read of cited pages, 2026-11-08
