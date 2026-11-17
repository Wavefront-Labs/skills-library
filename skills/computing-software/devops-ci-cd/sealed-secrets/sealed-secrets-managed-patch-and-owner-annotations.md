---
id: computing-software.devops-ci-cd.sealed-secrets.sealed-secrets-managed-patch-and-owner-annotations
name: sealed-secrets-managed-patch-and-owner-annotations
category: computing-software
field: devops-ci-cd
product: sealed-secrets
tags: [sealed-secrets, managed, patch, skip-set-owner-references, annotations, existing-secret, ownership]
level: advanced
status: docs-checked
description: "Control how the Sealed Secrets controller treats pre-existing Secrets using the managed, patch and skip-set-owner-references annotations."
sources: ["https://github.com/bitnami/sealed-secrets"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Sealed secrets managed patch and owner annotations

Three annotations on the Secret control how the controller treats an existing Secret.

`sealedsecrets.bitnami.com/managed: "true"` makes the controller manage an existing Secret. It is overwritten when a SealedSecret with the same name and namespace is unsealed, and the SealedSecret takes ownership, so deleting the SealedSecret also deletes the Secret.

`sealedsecrets.bitnami.com/patch: "true"` (new in v0.23.0) merges instead of replacing. Keys, labels and annotations present only in the existing Secret are kept; those in the SealedSecret are added; those present in both are overwritten by the SealedSecret. Patch alone does not give ownership. Combine `patch` with `managed` to get patching behaviour plus ownership.

`sealedsecrets.bitnami.com/skip-set-owner-references: "true"` keeps the SealedSecret and Secret independent: deleting the SealedSecret leaves the Secret behind. Set it on the Secret before sealing (the README says ahead of the Usage steps). Add `managed: "true"` too if the Secret should still be updated when the SealedSecret changes.

Choose by intent: replace and own (`managed`), add keys to a Secret created elsewhere (`patch`), or decouple lifetimes (`skip-set-owner-references`). 
## Checked
Date: 2026-11-04. Documentation: bitnami-labs/sealed-secrets README (raw markdown, main branch), sections Managing existing secrets, Patching existing secrets, Seal secret which can skip set owner references.
Confirmed: the three annotations, overwrite and ownership semantics, patch merge rules and v0.23.0, combining patch with managed, skip-set-owner-references with managed.
Removed: the default 'will not take over' claim and the claim about where the annotations are placed (not stated for managed/patch).
Method: documentation only; no commands were run.
