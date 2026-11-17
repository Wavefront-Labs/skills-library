---
id: computing-software.ai-ml-engineering.kubeflow.kubeflow-pipelines-pipeline-root
name: kubeflow-pipelines-pipeline-root
category: computing-software
field: ai-ml-engineering
product: kubeflow
tags: [pipeline-root, kfp-launcher, default-pipeline-root, object-store-root]
level: advanced
status: docs-checked
description: "Configure the KFP pipeline root at cluster (kfp-launcher ConfigMap), pipeline (@dsl.pipeline) and run level, with provider credential overrides per bucket prefix."
sources: ["https://github.com/kubeflow/website/blob/master/content/en/docs/components/pipelines/concepts/pipeline-root.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Pipelines pipeline root

A pipeline root is a path in an object store (SeaweedFS, S3, GCS) where run artifacts are written. Artifact metadata, including storage paths, is kept in an SQL database, separate from the pipeline root. Three levels; a pipeline-level root overrides the cluster default, and a run-level root overrides both:

1. **Cluster**: `ConfigMap/kfp-launcher` key `data.defaultPipelineRoot`. The manifest default is `minio://mlpipeline/v2/artifacts`. The same ConfigMap can carry provider credentials and per-prefix overrides:

```yaml
data:
  defaultPipelineRoot: gs://ml-models/
  providers: |-
    gs:
      default:
        credentials:
          fromEnv: false
          secretRef: {secretName: gs-secret-1, tokenKey: gs-tokenKey}
      overrides:
        - bucketName: ml-models
          keyPrefix: fraud-models
          credentials: {fromEnv: true}
```

Runs rooted at `gs://ml-models/fraud-models/` use the override credentials. The docs example places this ConfigMap in a user namespace.

2. **Pipeline**: `@pipeline(name=..., pipeline_root="gs://ml-models/recommendation/rank-model/")`.

3. **Run**: `client.create_run_from_pipeline_func(pipeline_func=..., pipeline_root="gs://.../sandbox")`, or the `pipeline-root` run parameter in the UI.

KFP does not create buckets or IAM policies; they must already exist. Components that write to storage themselves are possible but bypass KFP's artifact tracking.

## Checked

2026-11-09: confirmed against the Kubeflow website page "Pipeline Root" (content/en/docs/components/pipelines/concepts/pipeline-root.md, read in full): object stores, ConfigMap/kfp-launcher key `data.defaultPipelineRoot`, the manifest default, the providers and overrides example, `pipeline_root` in the pipeline decorator and in `create_run_from_pipeline_func`, the `pipeline-root` UI parameter. Removed the MLMD name and the multi-user claim, which that page does not state.

Method: docs-checked 2026-11-09 against the Kubeflow website pipeline-root page (raw markdown, read in full).
