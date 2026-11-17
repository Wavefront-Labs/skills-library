---
id: computing-software.ai-ml-engineering.kserve.kserve-storage-self-signed-ca
name: kserve-storage-self-signed-ca
category: computing-software
field: ai-ml-engineering
product: kserve
tags: [cabundle, cabundle-configmap, cabundlecrt, self-signed, verify-ssl, servingkserveios3-verifyssl, servingkserveios3-cabundle-configmap, cabundleconfigmapname, tls]
level: practitioner
status: docs-checked
description: "Make the storage initializer trust a self-signed model registry: global caBundleConfigMapName, per-namespace cabundle_configmap or annotation, or skip SSL verification."
sources: ["https://github.com/kserve/website/blob/main/docs/model-serving/storage/certificate/self-signed.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# CA bundles for self-signed storage endpoints

Works in Standard and Knative modes. (For ModelMesh use the `certificate` parameter in `storage-config`.)

## Global: every InferenceService
1. Create a ConfigMap in the namespace where the KServe controller runs; its data key MUST be `cabundle.crt`:
   `kubectl create configmap cabundle --from-file=/path/to/cabundle.crt`
2. In `inferenceservice-config`, set in the `storageInitializer` JSON: `"caBundleConfigMapName": "cabundle"`.
3. Restart the controller pod. The bundle is copied into each user namespace and attached to the storage-initializer.

## Per namespace: `storage-config` Secret
Create the ConfigMap (same `cabundle.crt` key) in the user namespace first, then either:
- annotate the Secret: `serving.kserve.io/s3-cabundle-configmap: local-cabundle`
- or add `"cabundle_configmap": "local-cabundle"` in the JSON entry (for example `localMinIO`, `"type": "s3"`).

## Skip verification (testing)
- annotation `serving.kserve.io/s3-verifyssl: "0"` (1 true, 0 false) on the Secret
- or `"verify_ssl": "0"` in the JSON entry (True/true/False/false also accepted).

## Checked
Method: docs-only read of cited pages, 2026-11-08

Read the cited KServe self-signed certificate page in full; every claim matches it. No content removed.
