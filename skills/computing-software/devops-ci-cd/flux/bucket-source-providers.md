---
id: computing-software.devops-ci-cd.flux.bucket-source-providers
name: bucket-source-providers
category: computing-software
field: devops-ci-cd
product: flux
tags: [bucket, s3, minio, sts, prefix]
level: sme
status: docs-checked
description: "Pull manifests from S3-compatible object storage, AWS, Azure or GCP with a Bucket source, using endpoint, prefix and STS."
sources:
  - https://fluxcd.io/flux/components/source/buckets/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A Bucket fetches manifests from object storage into an artifact that a Kustomization can apply.

`.spec.provider` is `generic` (default), `aws`, `azure` or `gcp`. Generic uses the Minio client SDK and works with S3-compatible stores such as Minio, Alibaba Cloud OSS, GCS interoperability and Wasabi; it requires a Secret reference.

Required: `.spec.bucketName`, `.spec.endpoint` (HTTP/S; a plain HTTP endpoint needs `.spec.insecure: true`) and `.spec.interval`. Some endpoints also need `.spec.region`.

```yaml
apiVersion: source.toolkit.fluxcd.io/v1
kind: Bucket
metadata:
  name: aws
  namespace: default
spec:
  interval: 5m0s
  provider: aws
  bucketName: podinfo
  endpoint: s3.amazonaws.com
  region: us-east-1
  timeout: 30s
```

Credentials: `.spec.secretRef.name` for static keys; for generic and aws the Secret has `accesskey` and `secretkey` data keys. Without a secret, the aws provider tries credentials retrieved from the AWS EC2 service (on EKS create an IAM role for the source-controller ServiceAccount that grants bucket access). Azure uses keys such as `accountKey`.

`.spec.sts` fetches temporary credentials: `provider: aws` (generic supports `ldap`) with an `endpoint`, and for LDAP a Secret with `username` and `password`.

`.spec.prefix` filters objects server-side (generic, aws and gcp only) and is preferred over `.spec.ignore` as a more efficient way of excluding files.

Inspect the artifact and conditions with `kubectl describe bucket NAME`.

## Checked

2026-11-08: read the source-controller Bucket spec (docs/spec/v1/buckets.md in the fluxcd/source-controller repo, the source of the fluxcd.io page) in part: the intro, providers, endpoint, STS, region, insecure, timeout, prefix and ignore sections, via search plus targeted reads. Confirmed: the provider list and generic default, required fields, plain HTTP needing insecure, accesskey and secretkey, aws default credentials and the EKS IAM role note, azure accountKey, STS providers (aws, and ldap for generic) with LDAP username and password, prefix support for generic, aws and gcp, and the kubectl describe step. Removed: nothing beyond rewording; the aws STS Secret detail is not claimed.

Method: documentation only; no commands were run.
