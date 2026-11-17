---
id: computing-software.search-and-information-retrieval.elasticsearch-opensearch.neural-search-ingest-models
name: neural-search-ingest-models
category: computing-software
field: search-and-information-retrieval
product: elasticsearch-opensearch
tags: [search-and-information-retrieval, elasticsearch-opensearch, elasticsearch, opensearch, neural-search-ingest-models]
level: advanced
status: docs-checked
description: "Register and deploy an ML Commons embedding model, embed text at ingest with the text_embedding processor, and search with the OpenSearch neural query."
sources:
  - https://raw.githubusercontent.com/opensearch-project/documentation-website/main/_vector-search/ai-search/semantic-search.md
  - https://docs.opensearch.org/latest/ingest-pipelines/processors/text-embedding/
  - https://docs.opensearch.org/latest/query-dsl/specialized/neural/
  - https://raw.githubusercontent.com/opensearch-project/documentation-website/main/_ml-commons-plugin/api/model-apis/register-model.md
  - https://raw.githubusercontent.com/opensearch-project/documentation-website/main/_ml-commons-plugin/api/model-apis/deploy-model.md
  - https://docs.opensearch.org/latest/ml-commons-plugin/cluster-settings/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Neural search with ML Commons models

**Goal:** generate embeddings inside the cluster at ingest and query time (OpenSearch; Elasticsearch has different inference features).

## 1. Register and deploy a model
- `POST _plugins/_ml/models/_register` registers a model. For a pretrained text embedding model the required body fields are `name`, `version` and `model_format` (`TORCH_SCRIPT` or `ONNX`). Registering a first version without `model_group_id` creates a model group automatically; the docs recommend registering a uniquely named group first. Registration returns a task, whose result gives the `model_id`.
- `POST _plugins/_ml/models/<model_id>/_deploy` loads the model into memory and returns a `task_id` (`DEPLOY_MODEL`); check `GET _plugins/_ml/tasks/<task_id>`. The optional `node_ids` list needs `plugins.ml_commons.allow_custom_deployment_plan` set to `true`. After a node or cluster restart the model must be redeployed.
- Local models run only on ML nodes by default (`plugins.ml_commons.only_run_on_ml_node` true); the docs recommend leaving it true in production.

## 2. Restrict where models come from
- Registering by URL (`plugins.ml_commons.allow_registering_model_via_url`) and from a local file (`...via_local_file`) are both off by default.
- If you enable URL registration, change `plugins.ml_commons.trusted_url_regex`: the docs call its default insecure (it allows any http, https, ftp or file URL). Set it to match only the repository holding your models.
- Optional: `plugins.ml_commons.model_access_control_enabled` (default false) turns on model group access control with the Security plugin.

## 3. Embed at ingest
- Pipeline: `{"text_embedding": {"model_id": "<model_id>", "field_map": {"passage_text": "passage_embedding"}}}`, created with `PUT _ingest/pipeline/<name>`.
- Creating the pipeline does not validate `model_id`; a missing or undeployed model only errors when a document is ingested. Test with `POST _ingest/pipeline/<name>/_simulate` first.
- A document without the input field is indexed without a vector, silently.
- Models truncate long input (BERT-style models are typically 512 tokens); split long documents first, for example with the `text_chunking` processor placed before `text_embedding`.
- Optional parameters include `batch_size` (default 1), `skip_existing` (default false), `ignore_failure` and `on_failure`.
- The index needs `index.knn: true`, the pipeline as `default_pipeline`, and the vector field as `knn_vector` whose `dimension` equals the model output (the docs example uses 768 with a `lucene` hnsw method).

## 4. Query
- `{"query":{"neural":{"passage_embedding":{"query_text":"...","model_id":"<model_id>","k":100}}}}`. Specify only one of `k`, `min_score` or `max_distance`; with none, `k` defaults to 10.
- `model_id` can be omitted if a default is set through a search pipeline with a `neural_query_enricher` request processor (`default_model_id`, or per field `neural_field_default_id`, which takes precedence) and `index.search.default_pipeline`. A `semantic` field type in the mapping avoids the ingest pipeline and `model_id` altogether.

## Verify
- [ ] `_simulate` returns a vector of the model's dimension.
- [ ] A query using the text of an indexed passage returns that passage first.

## Checked
2026-11-08. Confirmed from the OpenSearch documentation pages for semantic search, the text embedding processor, the neural query, the register and deploy model APIs, and the ML Commons cluster settings: the endpoints, required registration fields, `node_ids` setting, ML-node default, URL-registration settings and the insecure-default warning, processor parameters, truncation warning, no-validation and missing-field behaviour, neural query fields and `k` default, `neural_query_enricher`. Removed: the vague "allow-list" wording (the real setting is `trusted_url_regex`) and generic notes.
Method: documentation only; no commands were run.
