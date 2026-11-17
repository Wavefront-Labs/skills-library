---
id: computing-software.cloud-infrastructure-engineering.pulumi.kubernetes-server-side-apply
name: kubernetes-server-side-apply
category: computing-software
field: cloud-infrastructure-engineering
product: pulumi
tags: [cloud-infrastructure-engineering, pulumi, server-side-apply, ssa, field-manager, kubernetes-patch]
level: practitioner
status: docs-checked
description: "Pulumi Kubernetes server-side apply (SSA): the v4 default, benefits, Patch resource types, and the patchForce and patchFieldManager annotations."
sources:
  - https://www.pulumi.com/registry/packages/kubernetes/installation-configuration/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Server-side apply (SSA)

SSA is a Kubernetes resource management strategy introduced in Kubernetes v1.13: the API server computes diffs and resolves conflicts, so clients can safely share management of resources. The v4 release of the Pulumi Kubernetes provider manages resources using SSA by default.

Benefits per the docs:
- Resources may be safely managed by more than one controller.
- "Upsert": create the resource if absent, or apply configuration to an existing one.
- Every resource type in the SDK has a corresponding Patch resource type, to patch objects.
- The last-applied-configuration annotation is no longer used.

Annotations for SSA, set on the resource's metadata:
- `pulumi.com/patchForce`: force override of any conflicts for that resource.
- `pulumi.com/patchFieldManager`: the FieldManager name to use for the SSA operation.

In SSA mode the provider does not set the `app.kubernetes.io/managed-by` annotation.

## Gotchas
- Using `pulumi.com/skipAwait` during deletion is not recommended with SSA: it can cause race conditions during replacement.
- For the how-to (field conflicts, patching objects you do not own) use the provider's SSA how-to guide; this skill only records the points above.

## Checked
2026-11-03. Confirmed on the Kubernetes provider installation and configuration page (Server-Side Apply and Annotations sections). Removed: the `kubernetes:enableServerSideApply` setting, `ConfigMapPatch` coredns example, conflict message text, field manager name pattern, `kubectl --show-managed-fields` Verify and destroy-behaviour claims; the SSA how-to and blog page were not read.
Method: documentation only; no commands were run.
