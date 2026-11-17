---
id: computing-software.ai-ml-engineering.kserve.kserve-pmml-spark-mllib-serving
name: kserve-pmml-spark-mllib-serving
category: computing-software
field: ai-ml-engineering
product: kserve
tags: [pmml, pmmlserver, kserve-pmmlserver, spark-mllib, py4j, jpmml-sparkml, pyspark2pmml, containerconcurrency, openjdk]
level: practitioner
status: docs-checked
description: "Serve PMML and Spark MLlib models (via JPMML-SparkML) with the pmml modelFormat; pmmlserver is Py4J based, so no containerConcurrency: set cpu limit 1, scale replicas."
sources: ["https://github.com/kserve/website/blob/main/docs/model-serving/predictive-inference/frameworks/pmml/pmml.md", "https://github.com/kserve/website/blob/main/docs/model-serving/predictive-inference/frameworks/spark-mllib/spark-mllib.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# PMML and Spark MLlib on KServe

```yaml
spec:
  predictor:
    model:
      modelFormat: {name: pmml}
      storageUri: "gs://kfserving-examples/models/pmml"      # contains model.pmml
```

V1 request body is `{"instances": [[...]]}` to `/v1/models/NAME:predict`; the response includes class and probability fields (`Species`, `Probability_setosa`, `Node_Id`). For the Open Inference Protocol set `protocolVersion: v2` and `runtime: kserve-pmmlserver`.

## Performance
`pmmlserver` uses Py4J and has no multi-process mode, so you cannot set `spec.predictor.containerConcurrency`. To scale, set `resources.limits.cpu` to 1 and increase replicas.

## Local test
Needs OpenJDK 11. From `python/pmmlserver` run `uv sync`, then `python3 pmmlserver --model_dir /path/to/model_dir --model_name pmml-iris` (`--model_name` optional, default `model`).

## Spark MLlib
Spark models are served as PMML. Install `pyspark~=3.0.0` and `pyspark2pmml`, download the `jpmml-sparkml-executable-1.6.3.jar`, run `pyspark --jars <jar>`, fit a `Pipeline` (for example `RFormula` then `DecisionTreeClassifier`), export with `PMMLBuilder(spark, df, pipelineModel).buildFile("DecisionTreeIris.pmml")`, upload as `model.pmml`, then deploy with the same `pmml` format. Wait with `kubectl wait --for=condition=Ready inferenceservice spark-pmml`. The Spark page lists "pyspark 3.0.x or later"; the `~=3.0.0` pin is from its install command.

## Checked
Method: docs-only read of cited pages, 2026-11-08
Confirmed against the KServe website PMML and Spark MLlib pages: response field names, the Py4J no-multi-process warning and the CPU limit advice, OpenJDK 11 for local runs, `pmmlserver` arguments, jar version 1.6.3, `PMMLBuilder` usage, `kubectl wait`, and the v2 manifest with `kserve-pmmlserver`. No claims removed.
