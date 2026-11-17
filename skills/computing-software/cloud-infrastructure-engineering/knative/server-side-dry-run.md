---
id: computing-software.cloud-infrastructure-engineering.knative.server-side-dry-run
name: server-side-dry-run
category: computing-software
field: cloud-infrastructure-engineering
product: knative
tags: [dry-run, server-side-dry-run, admission-webhook, validate-manifest]
level: intro
status: docs-checked
description: "Validate and preview defaults for Services, Configurations and Routes without persisting them."
sources:
  - https://knative.dev/docs/serving/dryrun/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: check a Knative manifest and see defaulted fields before creating anything.

Kubernetes dry run asks the API server to admit, default and validate an object without persisting it to etcd. Use server-side dry run, `--dry-run=server`, which sends the request with the `dryRun=All` flag. The API server runs admission, defaulting and validation, including the Knative Serving webhooks.

What is validated:
- Knative Serving schema validation for `Service`, `Configuration`, `Route` and related objects.
- Knative defaulting webhooks apply defaults, for example missing `spec.template` fields; view them with `-o yaml`.
- Kubernetes admission and validation: quotas, RBAC, OpenAPI validation.

Limitations:
- Nothing is created or changed, controllers do not reconcile, and no Pods start.
- External systems are not contacted, so image digest resolution and runtime readiness checks do not happen.
- Feature gates and validations match a real request on your cluster's version and configuration.
- The Kubernetes server must support server-side dry run, GA since v1.18.

```bash
kubectl apply --dry-run=server -o yaml -f service.yaml
```

Read the printed YAML to see which defaults the webhook added. If dry run fails with validation errors, fix the reported fields and retry; RBAC errors mean your user lacks permission to create or update that kind in the namespace.

## Checked

Method: docs-checked 2026-11-09 against the Validating Resource Using Server-Side Dry Run page (raw markdown in knative/docs, read in full).
