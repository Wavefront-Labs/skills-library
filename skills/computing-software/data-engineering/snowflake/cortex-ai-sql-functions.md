---
id: computing-software.data-engineering.snowflake.cortex-ai-sql-functions
name: cortex-ai-sql-functions
category: computing-software
field: data-engineering
product: snowflake
tags: [snowflake, cortex-functions, cortex-ai, llm-functions, ai-sql]
level: advanced
status: docs-checked
description: "Choose and govern Snowflake Cortex AI Functions (AI_COMPLETE, AI_CLASSIFY, AI_FILTER, AI_AGG, AI_EMBED) on table data: privileges, cross-region routing, cost."
sources:
  - https://docs.snowflake.com/en/user-guide/snowflake-cortex/aisql
  - https://docs.snowflake.com/en/user-guide/snowflake-cortex/cross-region-inference
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cortex AI SQL functions

**Goal:** apply LLMs to rows in SQL (classify tickets, extract fields, summarise, embed for search) without moving data out of Snowflake. Models from several vendors run inside the Snowflake service perimeter. Availability is by region; some functions are Preview, so check each function's status before production use.

## Access
To call a Cortex AI Function the role needs the `USE AI FUNCTIONS` account-level privilege and one of the `CORTEX_USER` or `AI_FUNCTIONS_USER` database roles (see "Privileges and model access for Cortex AI Functions"). Do not assume a grant exists by default; check it.

## Pick the function
- `AI_COMPLETE`: generates a completion for text or an image with a chosen LLM; for most generative tasks.
- `AI_CLASSIFY`: classifies text or images into user-defined categories.
- `AI_FILTER`: returns TRUE or FALSE for text or image input; usable in SELECT, WHERE, or JOIN ... ON.
- `AI_AGG`: aggregates a text column into insights across rows from a prompt; not subject to context window limits. `AI_SUMMARIZE_AGG` does the same for summaries.
- `AI_EXTRACT`, `AI_SENTIMENT`, `AI_SUMMARIZE`, `AI_TRANSLATE`, `AI_REDACT` (PII), `AI_PARSE_DOCUMENT` (OCR or LAYOUT mode from a stage), `AI_TRANSCRIBE` (audio and video from a stage).
- `AI_EMBED` and `AI_MULTI_EMBED`: embedding vectors; `AI_SIMILARITY`: embedding similarity of two inputs.
- Helpers: `TO_FILE` (reference a staged file), `AI_COUNT_TOKENS` (check a prompt against a model limit), `PROMPT` (build prompt objects).
Look up exact argument lists and supported model names in each function's reference page; model availability differs by region.

## Cross-region inference
If a model is not deployed in your region, routing is controlled by the account parameter `CORTEX_ENABLED_CROSS_REGION`:
- `ANY_REGION` (global), cloud-specific values such as `AWS_GLOBAL`, `AZURE_GLOBAL`, `GCP_GLOBAL`, regional values such as `AWS_US`, `AWS_EU`, `AZURE_US`, or `DISABLED` (home region only, fewest models).
- Set it only with `ALTER ACCOUNT` as ACCOUNTADMIN (not ORGADMIN, not at user or session level). Check the value in effect with `SHOW PARAMETERS LIKE 'CORTEX_ENABLED_CROSS_REGION' IN ACCOUNT;`.
- If you have not set it, the account inherits a default (new organizations created after 2026-03-09 use `ANY_REGION`; other commercial accounts inherit a same-cloud geography value). Set it explicitly if you have data residency requirements.
- Customer data stays stored in your account region; prompt and response are sent transiently to the processing region and not persisted there. Between clouds, traffic crosses the public internet over mTLS. No egress charges.
```sql
ALTER ACCOUNT SET CORTEX_ENABLED_CROSS_REGION = 'AWS_US';
```

## Cost and performance
- LLM usage is billed in credits per the Snowflake Service Consumption Table; credits are consumed in the requesting region even when processed elsewhere. Do not hard-code prices.
- The functions are optimised for throughput over large tables (batch). For interactive, latency-sensitive use, the docs point to the REST APIs (Complete, Embed, Agents).
- Process new or changed rows only and store results rather than calling the functions in a BI view; use `AI_COUNT_TOKENS` to keep inputs within model limits.

## Quality
Evaluate on a labelled sample before rollout; store the prompt and model name next to results for reproducibility.

## Verify
Labelled sample accuracy meets the bar; the role has the required privileges; the cross-region parameter matches your residency policy.

## Checked
2026-11-09. Confirmed on "Snowflake Cortex AI Functions" and "Cross-region inference": function list and descriptions, required privilege and database roles, batch-versus-REST guidance, parameter values, default date, ACCOUNTADMIN-only, billing region, egress and mTLS notes. Removed because the fetched pages do not confirm them: the claim that CORTEX_USER is granted to PUBLIC by default, example calls with model names and argument shapes, the structured-output syntax, deprecation claims for the older function names, the usage-history view names, and the warehouse-size remark.
Method: documentation only; no commands were run.
