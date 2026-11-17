---
id: computing-software.cloud-infrastructure-engineering.jaeger.jaeger-es-ilm-support
name: jaeger-es-ilm-support
category: computing-software
field: cloud-infrastructure-engineering
product: jaeger
tags: [jaeger, ilm, jaeger-ilm-policy, es-use-ilm, is-write-index]
level: advanced
status: docs-checked
description: "Replace rollover cron jobs with an Elasticsearch ILM policy named jaeger-ilm-policy and init with ES_USE_ILM=true."
sources:
  - https://www.jaegertracing.io/docs/2.22/storage/elasticsearch/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: let Elasticsearch manage rollover and retention.

1. Create an ILM policy named `jaeger-ilm-policy`. The docs example rolls over the active index when older than 1m and deletes indices older than 2m:
```
curl -X PUT http://localhost:9200/_ilm/policy/jaeger-ilm-policy \
  -H 'Content-Type: application/json; charset=utf-8' --data-binary @- << EOF
{"policy":{"phases":{"hot":{"min_age":"0ms","actions":{"rollover":{"max_age":"1m"},"set_priority":{"priority":100}}},
"delete":{"min_age":"2m","actions":{"delete":{}}}}}}
EOF
```
(Those ages are for demonstration; pick real ones.)

2. Run the initializer with ILM enabled:
`docker run -it --rm --net=host -e ES_USE_ILM=true jaegertracing/jaeger-es-rollover:latest init http://localhost:9200`
It validates the policy exists, embeds `index.lifecycle.name` and `index.lifecycle.rollover_alias` in the templates, and sets `is_write_index: true` on write aliases.

3. Deploy Jaeger with `use_ilm: true` and `use_aliases: true` (and `create_mappings: false`).

You then no longer need the rollover, lookback or index-cleaner cron jobs.

Failure mode: if the policy is missing, init prints "ILM policy jaeger-ilm-policy doesn't exist in Elasticsearch. Please create it and rerun init".

## Checked

2026-11-03. Confirmed against the Elasticsearch page, ILM support section: policy name jaeger-ilm-policy and the example phases, ES_USE_ILM=true init, the validation, template and is_write_index steps, use_ilm with use_aliases, create_mappings false, the missing-policy error message and that the cron jobs are no longer needed. Removed: a closing paragraph that repeated the steps.
Method: documentation only; no commands were run.
