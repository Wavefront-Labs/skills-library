---
id: computing-software.cloud-infrastructure-engineering.keda.authentication-aws-secret-manager
name: authentication-aws-secret-manager
category: computing-software
field: cloud-infrastructure-engineering
product: keda
tags: [aws-secret-manager, awssecretmanager, secretkey, aws-pod-identity, access-key]
level: advanced
status: docs-checked
description: "Read scaler secrets from AWS Secrets Manager with the awsSecretManager TriggerAuthentication block, using pod identity or access keys."
sources:
  - https://keda.sh/docs/2.17/concepts/authentication/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The documentation introduces this integration as configuring the awsSecretManager key in your scaling specification. The secrets list defines the mapping between each AWS Secrets Manager secret and the authentication parameter the trigger uses, including parameter name, secret name, optional secretKey and optional version. Without a version the latest is used.
The `awsSecretManager` provider maps AWS Secrets Manager entries onto trigger parameters.

```yaml
awsSecretManager:
  podIdentity:
    provider: aws
  credentials:
    accessKey:
      valueFrom:
        secretKeyRef:
          name: {k8s-secret-with-aws-credentials}
          key: AWS_ACCESS_KEY_ID
    accessSecretKey:
      valueFrom:
        secretKeyRef:
          name: {k8s-secret-with-aws-credentials}
          key: AWS_SECRET_ACCESS_KEY
  region: {aws-region}
  secrets:
  - parameter: {param-name-used-for-auth}
    name: {aws-secret-name}
    version: {aws-secret-version}
    secretKey: {aws-secret-key}
```

Field meaning:
- `podIdentity.provider: aws` uses AWS pod identity instead of keys; the block is optional.
- `credentials` supplies an `accessKey` and an `accessSecretKey`, each read from a Kubernetes Secret through `valueFrom.secretKeyRef`. Optional block. The page's prose calls the second field `secretAccessKey` but its YAML uses `accessSecretKey`; the YAML name is used here.
- `region` is optional and falls back to the default region.
- `secrets` is required. Each item has a `parameter` and the AWS secret `name`; `version` is optional and defaults to the latest; `secretKey` is optional (the AWS secret key).

## Checked

2026-11-03. Confirmed on the 2.17 Authentication page: awsSecretManager block, podIdentity, credentials, region, secrets fields. Noted that the page prose says secretAccessKey while its YAML says accessSecretKey. Removed: the claim that secretKey selects among several values.

Method: documentation only; no commands were run.
