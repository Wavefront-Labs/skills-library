---
id: computing-software.search-and-information-retrieval.elasticsearch-opensearch.anomaly-detection-detectors
name: anomaly-detection-detectors
category: computing-software
field: search-and-information-retrieval
product: elasticsearch-opensearch
tags: [search-and-information-retrieval, elasticsearch-opensearch, elasticsearch, opensearch, anomaly-detection-detectors]
level: advanced
status: docs-checked
description: "Create an OpenSearch anomaly detector with a feature, detection interval and optional category field, preview it, and search results."
sources:
  - https://docs.opensearch.org/latest/observing-your-data/ad/api/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Anomaly detection detectors

**Goal:** find outliers in time series (OpenSearch Anomaly Detection plugin).
- Create with `POST _plugins/_anomaly_detection/detectors`. Required fields: `name`, `time_field`, `indices`, `feature_attributes` (a `feature_name`, `enabled` and an aggregation query) and `detection_interval`. Optional: `description`, `filter_query`, `window_delay`, `category_field`, `result_index`.
- Preview before starting: `POST _plugins/_anomaly_detection/detectors/_preview` with `period_start` and `period_end` and either a full `detector` object or a `detector_id`.
- `category_field` splits the data by a dimension, like `GROUP BY` in SQL, and the plugin keeps models for active entities in memory, so size the cluster for the number of active entities.
- Results go to the default result index, or to a custom one set with `result_index`. Search the default index with `POST _plugins/_anomaly_detection/detectors/results/_search/`; add the custom index name to the path to search it too.
- Use `window_delay` when you need extra processing time for data collection.

## Verify
- [ ] Preview over a window that contains a synthetic spike returns anomaly results for that window.

## Checked
Date: 2026-11-07
- OpenSearch Anomaly Detection API page (about 80 KB): read the create detector request and options table, the preview detector section (the `_preview` request with `detector_id`), the search detector result section, and located the memory and entity-count notes by search. Validate, update, start/stop, profile, stats and other sections were not read.
- Correction: the original used `POST _plugins/_anomaly_detection/detectors/<id>/_preview`; the page shows `POST _plugins/_anomaly_detection/detectors/_preview` with `detector_id` in the body (the id-in-path form appears only with the legacy `_opendistro` prefix).
- Removed: "Random Cut Forest" (not on the page), creation via Dashboards, the `.opendistro-anomaly-results*` index name guess, and the sparse-data claim.
Method: documentation only; no commands were run.
