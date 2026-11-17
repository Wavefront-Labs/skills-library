---
id: computing-software.search-and-information-retrieval.elasticsearch-opensearch.ilm-explain-and-troubleshooting
name: ilm-explain-and-troubleshooting
category: computing-software
field: search-and-information-retrieval
product: elasticsearch-opensearch
tags: [search-and-information-retrieval, elasticsearch-opensearch, elasticsearch, opensearch, ilm-explain-and-troubleshooting]
level: advanced
status: docs-checked
description: "Use ILM explain, step info, retry and start/stop to unstick indices in ERROR step."
sources:
  - https://www.elastic.co/docs/troubleshoot/elasticsearch/index-lifecycle-management-errors
  - https://www.elastic.co/docs/manage-data/lifecycle/index-lifecycle-management/policy-updates
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Troubleshoot stuck ILM

**Goal:** find why an index does not progress.
- `GET my-index/_ilm/explain` shows the current phase, action and step; `step_info` is returned only when further context is available (for example an error message). `GET _all/_ilm/explain?human=true&expand_wildcards=all&only_errors=true` lists indices in an error step.
- Rollover errors seen in the `ERROR` step include: `index.lifecycle.rollover_alias [x] does not point to index [y]`, `setting [index.lifecycle.rollover_alias] for index [y] is empty or not defined`, `alias [x] has more than one write index` (set `is_write_index: false` on all but one) and `index name [x] does not match pattern ^.*-\d+` (append digits such as `my-index-000001`).
- Migrate errors surface during shard recovery (for example `index has a preference for tiers [xxx] and node does not meet the required [xxx] tier`).
- After fixing the cause: `POST my-index/_ilm/retry`.
- Check the service: `GET _ilm/status`; `POST _ilm/stop` pauses all lifecycle policies (and also suspends SLM snapshots) and `POST _ilm/start` resumes them.
- A changed `min_age` in an updated policy is not propagated to the cached definition of indices already executing that phase.

## Verify
- [ ] Explain shows the index moving past the failed step (no `ERROR` step) after the retry.

## Scope
The Elasticsearch documentation was checked; OpenSearch (ISM) was not.

## Checked

Checked 2026-11-02 against the Elasticsearch docs pages Fix ILM errors, Policy updates and the ILM start/stop snippets. Confirmed: all statements above. Removed: "shrink on a node without space" and "policy not applied to old indices" as causes (not on the pages read), `POST _ilm/move` (not found in the docs source read), and the OpenSearch source root.

Method: documentation only; no commands were run.
