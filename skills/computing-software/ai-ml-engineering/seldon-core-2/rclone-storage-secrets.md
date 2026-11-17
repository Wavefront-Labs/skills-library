---
id: computing-software.ai-ml-engineering.seldon-core-2.rclone-storage-secrets
name: rclone-storage-secrets
category: computing-software
field: ai-ml-engineering
product: seldon-core-2
tags: [seldon-core-2, rclone, storage-secrets, secretname, s3, minio, gcs, seldon-agent-configmap, preloaded-secrets]
level: practitioner
status: docs-checked
description: "Give Seldon Core 2 servers access to model storage: rclone remote Secrets, Model secretName, preloaded secrets in the seldon-agent ConfigMap, and S3/MinIO and GCS examples."
sources: ["https://github.com/SeldonIO/seldon-core/blob/v2/docs-gb/kubernetes/storage-secrets.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Storage secrets with rclone

Servers fetch artifacts with Rclone from any supported backend (local, AWS S3, GCS and more). Public GCS buckets work out of the box through the Secret `seldon-rclone-gs-public`.

## Secret format
A remote has a name, a type and provider parameters. The prefix in `spec.storageUri` must equal the remote name. Use the rclone config format for parameters (for example GCS `client_id`). Each Secret holds exactly one rclone configuration under one data key.

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: minio-secret
  namespace: seldon-mesh
type: Opaque
stringData:
  s3: |
    type: s3
    name: s3
    parameters:
      provider: minio
      env_auth: false
      access_key_id: minioadmin
      secret_access_key: minioadmin
      endpoint: http://minio.minio-system:9000
```

## Two ways to use it
- Dynamic: set `spec.secretName: "minio-secret"` on the Model with `storageUri: "s3://models/iris"`.
- Preloaded: leave `secretName` empty and list the Secret in the `seldon-agent` ConfigMap `agent.json` under `rclone.config_secrets`. In helm use `config.agentConfig.rclone.configSecrets`; in a SeldonRuntime use `.spec.config.agentConfig.rclone.config_secrets`.

The ConfigMap applies to all Servers of the same SeldonRuntime, and the default includes `seldon-rclone-gs-public`. For GCS, put service account credentials in `service_account_credentials` with `type: gcs`.

## Checked

Confirmed against the Storage Secrets page: public GCS bucket secret seldon-rclone-gs-public, remote name matching the storageUri prefix, the config format for parameters, one configuration per Secret, dynamic spec.secretName versus preloaded secrets in the seldon-agent ConfigMap, the Helm and SeldonRuntime keys, the MinIO and GCS examples.

Method: docs-checked 2026-11-09 against the Seldon Core v2 docs-gb kubernetes/storage-secrets.md page (raw markdown).
