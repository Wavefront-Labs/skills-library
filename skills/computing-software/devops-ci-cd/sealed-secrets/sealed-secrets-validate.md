---
id: computing-software.devops-ci-cd.sealed-secrets.sealed-secrets-validate
name: sealed-secrets-validate
category: computing-software
field: devops-ci-cd
product: sealed-secrets
tags: [sealed-secrets, kubeseal, validate, decryption-error, ci]
level: intro
status: docs-checked
description: "Check that a SealedSecret can be decrypted by the controller using kubeseal --validate, and what the failure message looks like."
sources: ["https://github.com/bitnami/sealed-secrets"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Sealed secrets validate

`kubeseal --validate` validates whether an existing SealedSecret was properly created. Feed the manifest on stdin:

```console
$ cat sealed-secrets.yaml | kubeseal --validate
```

For an invalid SealedSecret, kubeseal prints:

```console
$ cat sealed-secrets.yaml | kubeseal --validate
error: unable to decrypt sealed secret
```

## Checked
Date: 2026-11-04. Documentation: bitnami-labs/sealed-secrets README (raw markdown, main branch), section Validate a Sealed Secret.
Confirmed: `--validate` flag, stdin usage, error text `error: unable to decrypt sealed secret`.
Removed: success-output claim, the list of failure causes and the restore paragraph (not in the README).
Method: documentation only; no commands were run.
