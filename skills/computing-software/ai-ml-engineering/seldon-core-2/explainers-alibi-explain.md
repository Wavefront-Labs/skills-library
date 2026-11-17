---
id: computing-software.ai-ml-engineering.seldon-core-2.explainers-alibi-explain
name: explainers-alibi-explain
category: computing-software
field: ai-ml-engineering
product: seldon-core-2
tags: [seldon-core-2, explainer, alibi-explain, anchor-tabular, anchor-text, modelref, pipelineref, explainability]
level: advanced
status: docs-checked
description: "Run Alibi-Explain black box explainers on MLServer as Model resources with spec.explainer: type, and exactly one of modelRef or pipelineRef."
sources: ["https://github.com/SeldonIO/seldon-core/blob/v2/docs-gb/explainers.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Explainers with Alibi-Explain

Explainers are Model resources with extra settings. They let explainers from the Alibi-Explain library run on MLServer.

```yaml
apiVersion: mlops.seldon.io/v1alpha1
kind: Model
metadata:
  name: income-explainer
spec:
  storageUri: "gs://seldon-models/scv2/samples/mlserver_1.5.0/income-sklearn/anchor-explainer"
  explainer:
    type: anchor_tabular
    modelRef: income
```

## Fields under spec.explainer
- `type`: one of the Alibi explainer types supported by the Alibi Explain runtime in MLServer (for example `anchor_tabular`, `anchor_text`).
- `modelRef`: model name for black box explainers.
- `pipelineRef`: pipeline name for black box explainers.

Only one of `modelRef` and `pipelineRef` is allowed.

## Explaining a pipeline
Black box explainers can explain a Pipeline as well as a Model:

```yaml
spec:
  storageUri: "gs://seldon-models/scv2/examples/huggingface/speech-sentiment/explainer"
  explainer:
    type: anchor_text
    pipelineRef: sentiment-explain
```

Documented examples: income classification with Anchor Tabular, a Huggingface sentiment pipeline with Anchor Text, and an Anchor Text movies sentiment explainer.

## Checked
Method: docs-checked 2026-11-09 against docs-gb/explainers.md (read in full). Dropped an unsupported claim about an alibi-explain requirement tag.
