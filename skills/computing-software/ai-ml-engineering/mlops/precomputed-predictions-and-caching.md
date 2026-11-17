---
id: computing-software.ai-ml-engineering.mlops.precomputed-predictions-and-caching
name: precomputed-predictions-and-caching
category: computing-software
field: ai-ml-engineering
product: mlops
tags: [mlops, batch-inference, precomputed-predictions, prediction-cache, online-store, feature-store, serving-fallback]
level: practitioner
status: draft
description: "Serve predictions from a precomputed table or key-value store with freshness SLAs, model-version keys, fallbacks for misses, and caching online inference results safely."
sources:
  - https://docs.aws.amazon.com/wellarchitected/latest/machine-learning-lens/machine-learning-lens.html
  - https://cloud.google.com/architecture/mlops-continuous-delivery-and-automation-pipelines-in-machine-learning
  - https://redis.io/docs/latest/develop/use/patterns/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Precomputed predictions and caching

**When:** the entity set is known and bounded (users, products, stores), predictions can be a few hours old, and serving latency must be single-digit ms. Recommendations, churn scores, demand forecasts, lead scores.

## Pattern
1. Scheduled batch job scores all entities (see distributed batch scoring).
2. Write to a serving store keyed by entity: Redis, DynamoDB, Bigtable, Cassandra, or a feature store's online store.
```text
key:   churn:v7:user:12345
value: {"score": 0.82, "model_version": "v7", "scored_at": "2026-10-16T02:10Z", "features_date": "2026-10-15"}
TTL:   48h (older than two cycles is treated as missing)
```
3. API reads the key; on miss (new user, expired, store outage) apply a fallback: online model call, segment-level default, or "unknown" handled by the product.
4. Publish atomically: write the new version under a new key prefix or table, validate counts and distributions, then flip a pointer (`churn:current -> v7`, a table alias, or config). Readers never see a half-written run.

## Freshness and coverage
- Track `scored_at` lag and coverage (% of active entities with a valid prediction) as SLOs; alert if the batch job fails and predictions age past the TTL.
- Entities created after the batch run need the fallback path - measure how often it is hit.

## Caching online inference
For expensive models with repeated identical inputs (LLM classification of the same text, embeddings of the same document):
- Key = hash(canonicalised input + model version + relevant params). Including the model version makes deploys naturally invalidate.
- Scope by tenant if inputs or outputs are tenant-specific.
- Do not cache predictions that depend on time-varying features unless the TTL matches feature freshness.
- Measure hit rate; a cache with 2% hits is cost without benefit.

## Gotchas
- Batch-scored features and online-path features drift apart; the fallback model must use the same feature definitions.
- Large writes to Redis/DynamoDB can throttle production traffic - rate-limit the loader or use bulk-load paths.

## Verify
- [ ] Prediction age and coverage dashboards exist and alert.
- [ ] Simulated store outage serves fallbacks within latency budget.
