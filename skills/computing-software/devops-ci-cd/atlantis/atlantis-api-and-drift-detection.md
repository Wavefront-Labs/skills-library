---
id: computing-software.devops-ci-cd.atlantis.atlantis-api-and-drift-detection
name: atlantis-api-and-drift-detection
category: computing-software
field: devops-ci-cd
product: atlantis
tags: [api, drift-detection, drift-remediation, api-secret, healthz, alpha]
level: sme
status: docs-checked
description: "Call the alpha Atlantis API for plan, apply, drift detection and remediation, locks and health endpoints."
sources: ["https://www.runatlantis.io/docs/api-endpoints"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Atlantis api and drift detection

The API is marked alpha and unstable. Main endpoints are disabled unless the server has an `api-secret`; send it as `X-Atlantis-Token: <ATLANTIS_API_SECRET>`.

- `POST /api/plan` and `POST /api/apply`: body fields `Repository`, `Ref`, `Type` (`Github` or `Gitlab`), `Projects`, `Paths` (objects with `Directory` and `Workspace`), `PR` (omit or 0 for a non-PR run). At least one of `Projects` or `Paths` is needed; tags, SHAs and ambiguous refs need `base_branch`. `Directory` must be a clean repo-relative path (HTTP 400 for absolute paths, `..`, backslashes or globs). Apply plans first, then applies projects one at a time even with `parallel_apply`. Non-PR requests fail closed on team allowlist denial and cannot satisfy `approved` or `mergeable`.

```json
{ "Repository": "repo-name", "Ref": "main", "Type": "Github",
  "Paths": [{ "Directory": ".", "Workspace": "default" }], "PR": 2 }
```

- Drift: needs `--enable-drift-detection`. `POST /api/drift/detect` (fields `repository`, `ref`, `type`, optional `projects` or `paths`, `include_plan_output`), `GET /api/drift/status` (always needs the token), `POST /api/drift/remediate` with `action` `plan` (default) or `apply`. Apply needs `--enable-drift-remediation`, cached drift with `has_drift: true`, and does not bypass `apply_requirements`.
- `GET /api/locks` lists locks and needs the token when a secret is set.
- `GET /status`, `GET /healthz` (liveness), `GET /readyz` (503 if a dependency such as Redis is down), and `/debug/pprof` with `--enable-profiling-api`.

Envelope error codes: VALIDATION_ERROR 400, UNAUTHORIZED 401, FORBIDDEN 403, NOT_FOUND 404, SERVICE_UNAVAILABLE 503.

## Checked

2026-11-03. Prose and identifiers confirmed against the official Atlantis docs page(s): API Endpoints. Removed or fixed: nothing needed removing.

Method: documentation only; no commands were run.
