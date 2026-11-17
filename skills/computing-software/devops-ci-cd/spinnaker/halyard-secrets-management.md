---
id: computing-software.devops-ci-cd.spinnaker.halyard-secrets-management
name: halyard-secrets-management
category: computing-software
field: devops-ci-cd
product: spinnaker
tags: [secrets, halyard, encrypted, s3, gcs, secret-engine, halconfig]
level: advanced
status: docs-checked
description: "Keep secrets out of Spinnaker configs with encrypted: and encryptedFile: syntax and the S3, GCS and AWS Secrets Manager engines."
sources:
  - https://spinnaker.io/docs/reference/secrets/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Spinnaker supports end-to-end secrets management so config files can live in a Git repository without plain-text secrets. You replace a secret in a config file with the syntax below, and Spinnaker reads (decrypts) it at start time.

**Syntax.** For literal values such as passwords and tokens:

```
encrypted:<secret engine>!<key1>:<value1>!<key2>:<value2>!...
```

For secret files such as kubeconfigs:

```
encryptedFile:<secret engine>!<key1>:<value1>!<key2>:<value2>!...
```

The key-value pairs vary with each secret engine; read the page for the engine you use. Example: in a `github` account block, set `token: encrypted:<secret engine>!<key1>:<value1>!...` instead of the token itself.

**Supported engines** (each has its own reference page): S3, GCS and AWS Secrets Manager. The framework is extensible. A Google Secrets Manager engine exists in the Spinnaker source (kork) but the reference page says it is not documented.

**Practice.** The config holds only the reference string; the secret value stays in the secret store. Check the engine's page for the parameters and the access the service needs to read it.

## Checked
2026-11-09. Confirmed on the current Spinnaker "Secrets" reference page: purpose, both syntaxes, decryption at start time, the engine list and the Google Secrets Manager note.
Removed because the current page no longer says so (the Halyard install flow was replaced by Kustomize-based docs): "from Spinnaker 1.14", Halyard decrypting for validation and printing encrypted profile values, the claim that `hal` commands cannot take encrypted values, `*-local.yml` use, and the `hal backup create` pairing.
Method: documentation only; no commands were run.
