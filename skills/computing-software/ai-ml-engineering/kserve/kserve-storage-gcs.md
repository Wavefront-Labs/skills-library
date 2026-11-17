---
id: computing-software.ai-ml-engineering.kserve.kserve-storage-gcs
name: kserve-storage-gcs
category: computing-software
field: ai-ml-engineering
product: kserve
tags: [gcs, gs, gcloud-application-credentialsjson, google-service-account, gcscreds]
level: practitioner
status: docs-checked
description: "Serve models from Google Cloud Storage: anonymous public buckets, or a service account key Secret (gcloud-application-credentials.json) attached to the predictor ServiceAccount."
sources: ["https://github.com/kserve/website/blob/main/docs/model-serving/storage/providers/gcs.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# GCS model storage

URI format: `gs://${BUCKET_NAME}/${PATH}`, for example `gs://kfserving-examples/models/tensorflow/flowers`.

Public bucket: with no credential the anonymous client is used.

Private bucket: authenticate with a Google service account key stored in a Secret whose key is `gcloud-application-credentials.json`. That key name is configurable in the configuration (the page does not name the file); if you change it, use the same name in the Secret.

```bash
kubectl create secret generic gcscreds \
  --from-file=gcloud-application-credentials.json=/path/to/gcloud-application-credentials.json
```

Declaratively: `type: Opaque` and `data: {gcloud-application-credentials.json: <base64 of key file>}`.

Attach it to a ServiceAccount and reference that from the predictor:

```yaml
apiVersion: v1
kind: ServiceAccount
metadata: {name: sa}
secrets:
  - name: gcscreds
---
apiVersion: serving.kserve.io/v1beta1
kind: InferenceService
metadata: {name: tensorflow-gcs}
spec:
  predictor:
    serviceAccountName: sa
    model:
      modelFormat: {name: tensorflow}
      storageUri: "gs://kfserving-examples/models/tensorflow/flowers"
```

## Checked
Method: docs-only read of cited pages, 2026-11-08

Read the cited GCS page in full. Removed the claim that the key name is set in inferenceservice-config; the page only says it is configurable in the configuration.
