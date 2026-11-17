---
id: computing-software.devops-ci-cd.sealed-secrets.sealed-secrets-scopes
name: sealed-secrets-scopes
category: computing-software
field: devops-ci-cd
product: sealed-secrets
tags: [sealed-secrets, scope, strict, namespace-wide, cluster-wide, kubeseal, rbac]
level: practitioner
status: docs-checked
description: "Choose between strict, namespace-wide and cluster-wide Sealed Secrets scopes, and set them with kubeseal --scope or annotations on the input Secret."
sources: ["https://github.com/bitnami/sealed-secrets"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Sealed secrets scopes

Scope controls what is bound into the encryption, so it decides whether a SealedSecret can be renamed or moved. Sealed Secrets behaves as if each namespace had its own key, but technically it includes the namespace name (and secret name) in the encrypted payload.

Scopes:
- `strict` (default): the secret must be sealed with exactly the same name and namespace. Both become part of the encrypted data; changing either causes a decryption error. This stops a user who can read a SealedSecret in one namespace from copying it to a namespace where they can read Secrets, and stops renaming it to overwrite a Secret they are allowed to see.
- `namespace-wide`: the sealed secret can be freely renamed within its namespace.
- `cluster-wide`: it can be unsealed in any namespace under any name.

Secret items (keys such as `spec.encryptedData.my-key`) can be renamed at will without losing decryptability.

Select the scope with a flag:

```bash
kubeseal --scope cluster-wide <secret.yaml >sealed-secret.json
```

Or annotate the input Secret: `sealedsecrets.bitnami.com/namespace-wide: "true"` or `sealedsecrets.bitnami.com/cluster-wide: "true"`. No annotation means strict; if both are set, cluster-wide wins. The README notes a later release will consolidate these into one `sealedsecrets.bitnami.com/scope` annotation.

Use wider scopes only when everyone with cluster access is an admin or cannot read Secrets at all, or when the namespace or name is not known up front (for example a hash-suffixed name).

## Checked
Date: 2026-11-04. Documentation: bitnami-labs/sealed-secrets README (raw markdown, main branch), section Scopes.
Confirmed: three scopes and semantics, `--scope`, the two annotations, cluster-wide precedence, item renaming, consolidated scope annotation note.
Removed: nothing.
Method: documentation only; no commands were run.
