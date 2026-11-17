---
id: computing-software.cloud-infrastructure-engineering.crossplane.function-desired-state
name: function-desired-state
category: computing-software
field: cloud-infrastructure-engineering
product: crossplane
tags: [function, desired-state, observed-state, server-side-apply, grpc]
level: advanced
status: docs-checked
description: "How a composition function receives observed state and must return the full desired state, which Crossplane applies with server-side apply."
sources:
  - https://docs.crossplane.io/latest/composition/compositions/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Each function is a gRPC server. Crossplane sends a RunFunctionRequest with the observed state (XR plus composed resources and their connection details), the desired state accumulated so far, the function input and the pipeline context. The function returns a RunFunctionResponse.

Key rules:

- Observed state is captured once before the pipeline, so every function sees the same observation.
- A function can change the XR `status` and the `metadata` and `spec` of composed resources. It cannot change the XR's `metadata` or `spec`, composed resource `status`, or composed connection details.
- The pipeline accumulates desired state. A function must copy all desired state from request to response, or Crossplane deletes the omitted composed resources. SDKs usually do this for you.
- Add the same fields every time. A field or composed resource omitted on a later call is deleted.
- Desired state is a fully specified intent applied with server-side apply, so include only fields you have an opinion about; omit status, labels and defaults.
- The XR becomes ready when the pipeline reports all composed resources ready.

Crossplane also fills `meta.capabilities` in the request, so a function can check a feature is supported before relying on it.

## Checked

Checked against the Compositions page, How composition functions work section (observed state, desired state, accumulation, server-side apply, capabilities), read in full.

Method: docs-checked 2026-11-09 against the composition/compositions page (docs repo raw markdown).
