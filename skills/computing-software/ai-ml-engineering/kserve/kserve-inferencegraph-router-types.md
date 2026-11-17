---
id: computing-software.ai-ml-engineering.kserve.kserve-inferencegraph-router-types
name: kserve-inferencegraph-router-types
category: computing-software
field: ai-ml-engineering
product: kserve
tags: [inferencegraph, routertype, sequence, switch, ensemble, splitter, gjson, condition, root-node, nodename, servicename]
level: intro
status: docs-checked
description: "InferenceGraph spec: routerType Sequence, Switch, Ensemble, Splitter, step targets, GJSON conditions, data: $response, root entrypoint, weights summing to 100."
sources: ["https://github.com/kserve/website/blob/main/docs/model-serving/inferencegraph/overview.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# InferenceGraph router types

`serving.kserve.io/v1alpha1` `InferenceGraph` has `spec.nodes.<name>` each with `routerType` and `steps`. The entrypoint node must be named `root`. A step has exactly one target: `serviceName` (InferenceService), `serviceUrl` (external) or `nodeName` (another node), plus optional `name` (unique in node), `condition` (GJSON), `data`, `weight`.

| routerType | Behaviour | Step fields |
|---|---|---|
| `Sequence` | run in order | optional `condition`, `data` |
| `Switch` | first matching condition only | `condition` required |
| `Ensemble` | all in parallel; response is an object keyed by step `name` | none |
| `Splitter` | one target by probability | `weight` required, must sum to 100 |

```yaml
apiVersion: serving.kserve.io/v1alpha1
kind: InferenceGraph
metadata: {name: sequential-processing-pipeline}
spec:
  nodes:
    root:
      routerType: Sequence
      steps:
        - {serviceName: preprocessor, name: preprocess_step}
        - {serviceName: classifier, name: classify, data: $response}
        - serviceName: text-classifier
          name: classify_text
          condition: "[@this].#(predictions.0.class==\"news\")"
```
- `data: $response` (the only supported value) passes the previous step output; default is the original node input for every step.
- In a Sequence, an unmet condition stops later steps.
- Switch example condition: `[@this].#(instances.0.data>0.5 && instances.0.data<=0.9)`.
- Nodes compose: a step can use `nodeName: choose` pointing at a Splitter or Ensemble node.

## Checked
Method: docs-only read of cited pages, 2026-11-08

Read the cited InferenceGraph overview page in full. Removed the no-match Switch behaviour and the router config section, neither of which is on that page.
