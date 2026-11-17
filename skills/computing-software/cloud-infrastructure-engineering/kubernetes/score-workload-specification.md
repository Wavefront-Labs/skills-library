---
id: computing-software.cloud-infrastructure-engineering.kubernetes.score-workload-specification
name: score-workload-specification
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, score-spec, humanitec, workload-specification, score-k8s, score-compose, platform-engineering]
level: practitioner
status: docs-checked
description: "Describe a workload once in score.yaml (containers, service ports, resource dependencies) and generate Compose or Kubernetes manifests with score-compose and score-k8s."
sources: ["https://docs.score.dev/docs/score-specification/score-spec-reference/", "https://github.com/score-spec/spec", "https://github.com/score-spec/spec/blob/main/score-v1b1.json", "https://github.com/score-spec/score-k8s", "https://github.com/score-spec/score-compose"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Score workload specification

Score is a developer-facing spec: what the workload needs, not how each
platform provides it. The same `score.yaml` drives local Compose and Kubernetes.

## score.yaml
```yaml
apiVersion: score.dev/v1b1
metadata:
  name: orders
containers:
  api:
    image: ghcr.io/acme/orders:1.8.0
    variables:
      DB_HOST: ${resources.db.host}
      DB_PASSWORD: ${resources.db.password}
      PUBLIC_URL: https://${resources.dns.host}
    resources:
      requests: {cpu: 250m, memory: 256Mi}
    readinessProbe:
      httpGet: {path: /ready, port: 8080}
service:
  ports:
    web: {port: 80, targetPort: 8080}
resources:
  db:
    type: postgres
  dns:
    type: dns
  route:
    type: route
    params: {host: "${resources.dns.host}", path: /, port: 80}
```
A container `image` of `.` is replaced by the `--image` value at generate time.

## Local: score-compose
```bash
score-compose init
score-compose generate score.yaml --image ghcr.io/acme/orders:dev
docker compose up -d
```
Default provisioners cover `postgres`, `dns`, `route` and more for local runs. Container
`resources` are validated but ignored by Compose.

## Kubernetes: score-k8s
```bash
score-k8s init                                    # writes .score-k8s/ state and default provisioners
score-k8s generate score.yaml --image ghcr.io/acme/orders:1.8.0
kubectl apply -f manifests.yaml
```
Generates the workload (a Deployment by default) plus whatever the provisioner for each
resource type emits. Provisioners load from `*.provisioners.yaml` in `.score-k8s/` (or
`score-k8s init --provisioners <uri>`) and match by `type` (plus optional `class`, `id`) with
first-match precedence, so platform teams override defaults with their own (e.g.
`type: postgres` -> an operator CRD), and developers never see those details.

## Where it fits
- Good for: many similar stateless services, consistent dev/prod wiring, hiding Kubernetes
  YAML from app teams.
- Weak for: workloads needing fine-grained Kubernetes features (custom scheduling,
  sidecars). score-k8s emits a StatefulSet when the workload annotation
  `k8s.score.dev/kind: StatefulSet` is set, and `score-k8s init --patch-templates` applies
  template-generated `set`/`delete` patches to the output; use plain manifests beyond that.

## Verify
- [ ] The same `score.yaml` works locally and in a dev cluster; generated manifests pass
  policy checks (kubeconform, Kyverno CLI) in CI before apply.

## Checked
2026-10-27, against the Score spec repo (score-spec/spec main: README and `score-v1b1.json`) and the score-k8s and score-compose READMEs (main). Confirmed: `apiVersion: score.dev/v1b1`, container `variables`, `resources.requests`, `readinessProbe.httpGet`, `service.ports` with `port`/`targetPort`, resource `type`/`params`, `${resources.<id>.<output>}` placeholders, `postgres`/`dns`/`route` default provisioner outputs and params, `init`/`generate --image` for both tools, `manifests.yaml`, provisioner file matching, `--patch-templates`, the `k8s.score.dev/kind` annotation.
Method: documentation only; no commands were run.
