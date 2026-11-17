---
id: computing-software.ai-ml-engineering.kserve.kserve-config-storage-credentials
name: kserve-config-storage-credentials
category: computing-software
field: ai-ml-engineering
product: kserve
tags: [storageinitializer, enablemodelcar, cabundleconfigmapname, storagespecsecretname, servingkserveiostoragesecretname, servingkserveios3-endpoint, s3usehttps, s3verifyssl, s3useanoncredential, storagekserveioreadonly, storage-initializer-uid]
level: advanced
status: docs-checked
description: "Storage initializer and credentials keys in inferenceservice-config: resource defaults, CA bundle, modelcar, secret-name precedence, S3 annotations, PVC read-only annotation."
sources: ["https://github.com/kserve/website/blob/main/docs/admin-guide/configurations.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# inferenceservice-config: storageInitializer and credentials

## storageInitializer
Defaults: `memoryRequest` 100Mi, `memoryLimit` 1Gi, `cpuRequest` 100m, `cpuLimit` 1, `caBundleConfigMapName` empty, `caBundleVolumeMountPath` `/etc/ssl/custom-certs`, `enableModelcar` true (enables `oci://` URIs), `cpuModelcar` 10m and `memoryModelcar` 15Mi (request and limit of the passive modelcar container), `uidModelcar` 1010 (user ID of the modelcar process and main container). The image and the four request/limit values are overridden by a `ClusterStorageContainer` when one exists.

Per-service annotations: `storage.kserve.io/readonly` (default `true`; set `false` to mount the PVC read-write; no global key), `serving.kserve.io/storage-initializer-uid` (default 1000; the user ID of the storage initializer init container, useful when Istio CNI with DNS proxy is enabled).

## credentials
```json
{"storageSpecSecretName": "storage-config",
 "storageSecretNameAnnotation": "serving.kserve.io/storageSecretName",
 "gcs": {"gcsCredentialFileName": "gcloud-application-credentials.json"},
 "s3": {"s3AccessKeyIDName": "AWS_ACCESS_KEY_ID", "s3SecretAccessKeyName": "AWS_SECRET_ACCESS_KEY",
        "s3Endpoint": "", "s3UseHttps": "", "s3Region": "", "s3VerifySSL": "",
        "s3UseVirtualBucket": "", "s3UseAccelerate": "", "s3UseAnonymousCredential": "", "s3CABundle": ""}}
```

Secret precedence: with `storageUri`, the secret-name annotation beats secrets referenced by the service account; with `storageSpec`, the annotation beats `storageSpecSecretName`.

S3 settings can be overridden by annotations placed on the ServiceAccount or Secret (not the InferenceService): `serving.kserve.io/s3-endpoint`, `s3-usehttps` ("0"/"1"), `s3-region`, `s3-verifyssl`, `s3-usevirtualbucket`, `s3-useaccelerate`, `s3-useanoncredential`, `s3-cabundle`. `s3AccessKeyIDName`/`s3SecretAccessKeyName` apply only to static IAM-user keys (IAM User Access Key Secret); the other S3 fields apply to both that and IAM Role for Service Account when non-empty.

## Checked
Confirmed against the KServe Configurations admin guide: every storageInitializer default, the readonly and storage-initializer-uid annotations, the credentials JSON block, secret-name precedence for storageUri and storageSpec, the S3 override annotations and the ServiceAccount or Secret placement note. Clarified the modelcar and PVC read-write wording.

Method: docs-only read of cited pages, 2026-11-08
