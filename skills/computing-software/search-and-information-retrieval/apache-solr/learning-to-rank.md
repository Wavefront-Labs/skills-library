---
id: computing-software.search-and-information-retrieval.apache-solr.learning-to-rank
name: learning-to-rank
category: computing-software
field: search-and-information-retrieval
product: apache-solr
tags: [ltr, learning-to-rank, feature-store, model-store, feature-logging]
level: sme
status: docs-checked
description: "Rerank Solr results with the Learning to Rank module: feature and model stores, feature and model classes, the ltr rq parser and feature logging."
sources:
  - https://solr.apache.org/guide/solr/latest/query-guide/learning-to-rank.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# learning-to-rank

LTR re-ranks the top documents with a trained model. Train the model outside Solr; Solr hosts features and models and can log feature values.

Enable: start with `-Dsolr.modules=ltr -Dsolr.ltr.enabled=true` (the module needs `modules/ltr/lib/solr-ltr-*.jar`), and declare the `[features]` transformer in `solrconfig.xml`.

Stores are managed over REST:
- Features: PUT to `/schema/feature-store`, read at `/schema/feature-store/<store>`.
- Models: `/schema/model-store`. DELETE a model or store by name; a model must be deleted before its feature store.

Feature classes include `SolrFeature` (query-based), `FieldValueFeature` (set a `defaultValue` only if the schema field has no default) and `ValueFeature`. Model classes include `LinearModel` and `MultipleAdditiveTreesModel`.

Rank: `rq={!ltr model=currentModel reRankDocs=100}`.

Log features for training: `fl=id,score,[features store=nextFeatureStore]`.

Re-ranking only reorders the top `reRankDocs` documents.

## Checked

Checked 2026-11-09 against the full Learning To Rank page of the Solr Reference Guide: module enabling properties, feature and model store endpoints, delete order, feature and model classes, FieldValueFeature defaultValue caution, rq and fl examples. The query-re-ranking source was not read and was dropped.

Method: docs-checked 2026-11-09 against the Learning To Rank page (raw ref-guide source); no commands were run.
