---
id: computing-software.devops-ci-cd.sealed-secrets.sealed-secrets-manual-key-management-and-reencrypt
name: sealed-secrets-manual-key-management-and-reencrypt
category: computing-software
field: devops-ci-cd
product: sealed-secrets
tags: [sealed-secrets, manual-key-management, re-encrypt, sealing-key-label, shared-key, multi-cluster]
level: sme
status: docs-checked
description: "Manage Sealed Secrets sealing keys by hand, share one key across clusters, relabel keys, and re-encrypt files with kubeseal --re-encrypt before retiring old keys."
sources: ["https://github.com/bitnami/sealed-secrets"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Sealed secrets manual key management and reencrypt

Sealing keys are plain Kubernetes Secrets in the controller's namespace (usually `kube-system`, but configurable), labelled `sealedsecrets.bitnami.com/sealed-secrets-key`. You can create, move or delete them, but the README advises not deleting old keys unless you know what you are doing.

Uses of creative key management: share the same sealing key among several clusters so one SealedSecret applies to all of them; because keys are ordinary Secrets you can even manage them via GitOps with sealed secrets themselves.

Relabelling: setting the label to anything other than `active` effectively removes the key from the controller, although it stays in Kubernetes for manual encryption or decryption. The controller does not pick up manually created, deleted or relabelled keys on its own; an administrator must restart the controller.

Re-encryption comes before key cleanup:

```bash
kubeseal --re-encrypt <my_sealed_secret.json >tmp.json && mv tmp.json my_sealed_secret.json
```

This produces a file encrypted with the latest key without the plaintext leaving the cluster to the client. It does not update the in-cluster object, so save the new file in version control. Old keys are not garbage collected automatically.

Re-encrypting periodically is sensible but gives false security if the old file version is still reachable by an attacker.

## Checked
Date: 2026-11-04. Documentation: bitnami-labs/sealed-secrets README (raw markdown, main branch), sections Manual key management, Re-encryption.
Confirmed: keys are Secrets labelled `sealedsecrets.bitnami.com/sealed-secrets-key`, shared keys, relabel behaviour, restart requirement, `kubeseal --re-encrypt` command and semantics, no key garbage collection.
Removed: 'and apply it' (the README only says to save the file in version control).
Method: documentation only; no commands were run.
