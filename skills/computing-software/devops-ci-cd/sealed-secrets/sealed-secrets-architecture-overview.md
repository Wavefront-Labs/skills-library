---
id: computing-software.devops-ci-cd.sealed-secrets.sealed-secrets-architecture-overview
name: sealed-secrets-architecture-overview
category: computing-software
field: devops-ci-cd
product: sealed-secrets
tags: [sealed-secrets, kubeseal, controller, sealedsecret, asymmetric-encryption, gitops]
level: intro
status: docs-checked
description: "Explain how Sealed Secrets works: a cluster controller, the kubeseal client, asymmetric encryption and the SealedSecret resource that unseals into a normal Secret."
sources: ["https://github.com/bitnami/sealed-secrets"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Sealed secrets architecture overview

Sealed Secrets has two parts: a cluster-side controller (operator) and the client utility `kubeseal`. `kubeseal` uses asymmetric crypto to encrypt a Secret so that only the controller can decrypt it. The result is a `SealedSecret` custom resource (`apiVersion: bitnami.com/v1alpha1`), which you can treat as a recipe for creating a Secret.

```yaml
apiVersion: bitnami.com/v1alpha1
kind: SealedSecret
metadata:
  name: mysecret
  namespace: mynamespace
spec:
  encryptedData:
    foo: AgBy3i4OJSWK+PiTySYZZA9rO43cGDEq.....
```

Within a few seconds of applying it, the controller creates an ordinary Kubernetes Secret with the same name and namespace and the decoded data (`foo: YmFy` is base64 of `bar`). Pods consume it like any other Secret.

Key facts to hold onto:
- The encrypted resource is safe to store in Git, even a public repository, because from the end user's point of view a SealedSecret is a write-only device: nobody, not even the author, can recover the plaintext from it.
- The controller keeps private/public key pairs as Kubernetes Secrets labelled `sealedsecrets.bitnami.com/sealed-secrets-key`, marked `active` or `compromised`. On startup it loads active keys, creates a new key, and starts the renewal cycle.
- The generated Secret is a dependent object of the SealedSecret: it is updated and deleted along with it.
- The scheme does not authenticate users. Anyone can create a SealedSecret with matching name and namespace, so cluster RBAC and your config-management workflow must control what gets applied.

## Checked
Date: 2026-11-04. Documentation: bitnami-labs/sealed-secrets README (raw markdown, main branch), sections Overview, Scopes, Usage, Details (advanced).
Confirmed: two components, asymmetric crypto, `bitnami.com/v1alpha1` example, base64 example, key labels active/compromised, startup sequence, dependent object, no user authentication.
Removed: nothing.
Method: documentation only; no commands were run.
