---
id: computing-software.ai-ml-engineering.kserve.kserve-storage-s3
name: kserve-storage-s3
category: computing-software
field: ai-ml-engineering
product: kserve
tags: [s3, s3-credentials, iam-role-for-service-account, eksamazonawscomrole-arn, aws-access-key-id, s3-max-file-concurrency, minio, holdapplicationuntilproxystarts, servingkserveios3-region]
level: practitioner
status: docs-checked
description: "Serve models from S3 or S3-compatible storage (MinIO): IAM role service account vs access-key Secret, s3-* annotations, download concurrency, Istio sidecar race fix."
sources: ["https://github.com/kserve/website/blob/main/docs/model-serving/storage/providers/s3/s3.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# S3 model storage

Two credential methods: IAM Role for Service Account (recommended) or IAM user keys. Global fallbacks come from the inferenceservice ConfigMap; annotations on the Secret or ServiceAccount win.

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: sa
  annotations:
    eks.amazonaws.com/role-arn: arn:aws:iam::123456789012:role/s3access
    serving.kserve.io/s3-endpoint: s3.amazonaws.com   # e.g. minio-service.kubeflow:9000
    serving.kserve.io/s3-usehttps: "1"                # 0 for plain-HTTP MinIO
    serving.kserve.io/s3-region: "us-east-2"
    serving.kserve.io/s3-useanoncredential: "false"   # true ignores credentials
```

User-key variant: an `Opaque` Secret carrying the same annotations and `AWS_ACCESS_KEY_ID` / `AWS_SECRET_ACCESS_KEY` in `stringData`, referenced from the ServiceAccount `secrets:` list.

```yaml
spec:
  predictor:
    serviceAccountName: sa
    model:
      modelFormat: {name: tensorflow}
      storageUri: "s3://kserve-examples/mnist"
```

Tuning: the `ClusterStorageContainer` env `S3_MAX_FILE_CONCURRENCY` (default 4) sets how many files download in parallel; each parallel download forks Python and creates a boto3 client.

Gotcha: with Istio sidecars you may see `tcp dial connection refused` when the agent pulls from S3 before the proxy is ready. Set `proxy.holdApplicationUntilProxyStarts: true` in the `istio-sidecar-injector` ConfigMap (introduced in Istio 1.7 as an experimental feature, off by default).

## Checked
Method: docs-only read of cited pages, 2026-11-08
Confirmed against the KServe website S3 storage page: both credential methods, annotation names and defaults, Secret and ServiceAccount layout, `S3_MAX_FILE_CONCURRENCY` default of 4, and the Istio race note. Reworded the global-fallback source to the ConfigMap the page names without a block name.
