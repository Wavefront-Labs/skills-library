---
id: computing-software.ai-ml-engineering.kubeflow.kubeflow-pipelines-object-store-config
name: kubeflow-pipelines-object-store-config
category: computing-software
field: ai-ml-engineering
product: kubeflow
tags: [object-store, seaweedfs, objectstoreconfig, irsa, api-server-storage]
level: advanced
status: docs-checked
description: "Configure the object store for the KFP API server and launcher: SeaweedFS default since 2.15, supported providers, static credentials and AWS IRSA."
sources: ["https://github.com/kubeflow/website/blob/master/content/en/docs/components/pipelines/operator-guides/configure-object-store.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Pipelines object store config

Two KFP components use object storage: the API server (stores the pipeline IR) and the KFP launcher or executor (writes run artifacts). From KFP 2.15 the default object store in the Community Distribution is SeaweedFS, replacing the previous default. You need admin access to the KFP namespace and credentials for your provider.

API server support table:
- SeaweedFS with static credentials: yes; SeaweedFS gateway to AWS, GCP, Azure or Minio S3: yes.
- AWS S3 with static credentials: yes; AWS S3 with IRSA: yes.
- Other S3-compliant storage with static credentials: yes.
- Google Cloud Storage with static or application credentials: no.

Static credentials are long-lived access keys (for AWS, Access Key ID and Secret Access Key). Configure them with environment variables on the `ml-pipeline-api-server` container of the `ml-pipeline` Deployment in the KFP namespace: `OBJECTSTORECONFIG_HOST` (for example `s3.amazonaws.com`), `OBJECTSTORECONFIG_PORT`, `OBJECTSTORECONFIG_REGION`, `OBJECTSTORECONFIG_SECURE`, and `OBJECTSTORECONFIG_ACCESSKEY` and `OBJECTSTORECONFIG_SECRETACCESSKEY` read from a Kubernetes secret deployed beforehand. For IRSA, omit the access key variables (they take precedence, and if present the API server ignores IRSA) and associate the appropriate IAM role with the Kubernetes service account `ml-pipeline`; how depends on the platform, for example EKS has its own IRSA docs.

The launcher supports the same providers, plus Google Cloud Storage with static or application credentials. It is configured through `ConfigMap/kfp-launcher`:

- The ConfigMap must be in the namespace where pipelines run: the KFP namespace in a standalone deployment, or the user profile namespace in a Kubeflow Community Distribution deployment.
- `defaultPipelineRoot` defaults to `minio://mlpipeline/v2/artifacts`, where `mlpipeline` is the bucket name. Change it to store artifacts at another path.
- To use another provider add a `providers` field. The provider is chosen by the pipeline root scheme (`s3://` uses `s3`, `gs://` uses `gs`). The `s3` provider is valid for any S3-compliant storage and takes `endpoint`, `disableSSL`, `region`, `forcePathStyle` and `credentials`; `gs` takes only `credentials`.
- `credentials` is either `fromEnv: true` (IRSA or credentials in the task environment) or `fromEnv: false` with a `secretRef` (`secretName` plus `accessKeyKey` and `secretKeyKey` for S3, or `tokenKey` for GCS).
- `overrides` give different settings for a `bucketName` and `keyPrefix` within the pipeline root; fields not set fall back to `default`.

## Checked

2026-11-09: confirmed against the Kubeflow website page "Object Store Configuration" (content/en/docs/components/pipelines/operator-guides/configure-object-store.md, read in full): SeaweedFS default from 2.15, both provider tables, API server environment variables, IRSA precedence rule, kfp-launcher ConfigMap fields and overrides. Removed the unconfirmed instruction to annotate the service account and the generic consistency advice.

Method: docs-checked 2026-11-09 against the Kubeflow website configure-object-store page (raw markdown, read in full).
