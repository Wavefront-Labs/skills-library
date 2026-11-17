---
id: computing-software.cloud-infrastructure-engineering.opa-gatekeeper.opa-gatekeeper-admission-review-input
name: opa-gatekeeper-admission-review-input
category: computing-software
field: cloud-infrastructure-engineering
product: opa-gatekeeper
tags: [opa-gatekeeper, input-review, admission-request, userinfo, namespaceobject, oldobject, audit]
level: practitioner
status: docs-checked
description: "Know the fields of input.review that Gatekeeper passes to policies, and which of them are unavailable during audit."
sources: ["https://github.com/open-policy-agent/gatekeeper/blob/master/website/docs/input.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Opa gatekeeper admission review input

Policies receive the Kubernetes admission request as `input.review`. Fields:
- `dryRun`: whether the request came from `kubectl --dry-run`.
- `kind`: group, version, kind of the object.
- `name`: may be empty when the API server generates the name.
- `namespace`: empty for cluster-scoped objects.
- `namespaceObject`: full Namespace object (Rego `input.review.namespaceObject`, CEL `namespaceObject`); null for cluster-scoped.
- `object`: the object being created or modified.
- `oldObject`: previous state, only for UPDATE.
- `operation`: CREATE, UPDATE and so on.
- `uid`: request identifier.
- `userInfo`: `username`, `uid`, `groups`, `extra`.

The wire format is an `AdmissionReview` with the request under `request`, including `resource` (group, version, resource) alongside `kind`.

Audit gotcha: Kubernetes cannot populate `dryRun`, `operation`, `uid` or `userInfo` when Gatekeeper audits existing objects. Templates that depend on them are not auditable, and the Rego author must handle the unset case, otherwise every matching resource may be reported as violating.

## Checked

2026-11-08. Confirmed against input.md (field list, namespaceObject Rego and CEL names, audit limitation note, example AdmissionReview with request.resource). Read in full. Removed or corrected: nothing.

Method: documentation only; no commands were run.
