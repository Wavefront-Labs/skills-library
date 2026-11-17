---
id: computing-software.database-administration.neo4j.link-prediction-pipelines
name: link-prediction-pipelines
category: computing-software
field: database-administration
product: neo4j
tags: [neo4j, link-prediction-pipeline, node-classification-pipeline, gds-pipeline, graph-database, cypher, nosql]
level: practitioner
status: docs-checked
description: "Train and apply GDS link prediction pipelines: split config, node property and feature steps, train metrics, model catalog and disk storage"
sources: ["https://neo4j.com/docs/cypher-manual/current/", "https://neo4j.com/docs/operations-manual/current/", "https://github.com/neo4j/graph-data-science/blob/master/doc/modules/ROOT/pages/machine-learning/linkprediction-pipelines/link-prediction.adoc", "https://github.com/neo4j/graph-data-science/blob/master/doc/modules/ROOT/pages/machine-learning/linkprediction-pipelines/config.adoc", "https://github.com/neo4j/graph-data-science/blob/master/doc/modules/ROOT/pages/machine-learning/linkprediction-pipelines/training.adoc", "https://github.com/neo4j/graph-data-science/blob/master/doc/modules/ROOT/pages/model-catalog/store.adoc"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ML pipelines (link prediction)

Goal: train a model in the Graph Data Science (GDS) library that predicts where relationships should exist. The pipeline procedures are in the beta tier (`gds.beta.pipeline.linkPrediction.*`).

1. `gds.beta.pipeline.linkPrediction.create` the pipeline, then add `addNodeProperty` steps (GDS algorithms that write node properties), `addFeature` steps (combine the properties of a node pair into a link feature) and model candidates (`addLogisticRegression`, `addRandomForest`). Optionally `configureSplit`.
2. Train with `gds.beta.pipeline.linkPrediction.train(graphName, {modelName, pipeline, targetRelationshipType, ...})`. `modelName` must not already exist in the model catalog, `targetRelationshipType` must be undirected, `metrics` defaults to `AUCPR`, `randomSeed` makes runs repeatable. Parallel runs of one pipeline on one graph are not supported.
3. Predict with `gds.beta.pipeline.linkPrediction.predict.*` using the trained model (not the pipeline); it can run on a different graph and returns predicted probabilities.

Leakage control is built in: positive relationships are split into test, train and feature-input sets, with sampled negatives (`negativeSamplingRatio`) added to test and train. Node property steps see only the feature-input relationships (plus any context relationships you configure), so the target relationship is not used as a feature. Candidates are compared with stratified k-fold cross-validation (`validationFolds`); the winner is retrained and scored on train and on the held-out test set.

Persist models: the catalog is in-memory and lost on restart. `gds.model.store` writes to disk (Enterprise Edition feature, needs `gds.model.store_location` in `neo4j.conf`); train can do it automatically with `storeModelToDisk: true`.

Verify: the test-set metric in the train result (`modelInfo`) meets your target.

## Checked
2026-11-09

Method: read GDS repo docs pages for link prediction pipelines (overview, config, training) and model-catalog/store (raw asciidoc). Removed: the "confirm" hedges on naming and Enterprise status (both confirmed) and the unverified "AUC" target wording (default metric is AUCPR). Not checked: predict.adoc parameters in detail, node classification pipelines (named only in tags).
