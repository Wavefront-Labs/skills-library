---
id: computing-software.cloud-infrastructure-engineering.docker.compose-to-kubernetes-handoff
name: compose-to-kubernetes-handoff
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, compose, kompose, compose-to-kubernetes, kubernetes-migration, kubernetes, manifests, deployment, service, persistentvolumeclaim, configmap, helm, migration]
level: advanced
status: docs-checked
description: "Move a Compose stack to Kubernetes: what kompose convert maps and drops, the concept mapping (service, volume, env_file, restart) and the hand-fix list."
sources: ["https://kompose.io/user-guide/", "https://kompose.io/conversion/", "https://github.com/kubernetes/kompose", "https://kubernetes.io/docs/tasks/configure-pod-container/translate-compose-kubernetes/", "https://docs.docker.com/desktop/use-desktop/kubernetes/", "https://docs.docker.com/compose/bridge/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# From Compose to Kubernetes

**Goal:** turn a working Compose stack into Kubernetes manifests you understand and would
have written by hand, using kompose only as a first draft.

## Concept mapping
| Compose | Kubernetes | Notes |
|---|---|---|
| `services.<name>` | `Deployment` + `Service` (ClusterIP) | one Pod template per service |
| `image:` | `containers[].image` | `build:` has no equivalent, push first |
| `ports: ["80:8080"]` | `Service.ports` (+ `Ingress` for HTTP) | host port binding is not a thing; `type: NodePort/LoadBalancer` or Ingress |
| `expose:` | `Service.ports` without external exposure | |
| `environment:` | `env:` / `envFrom: configMapRef` | |
| `env_file:` | ConfigMap or Secret you create | keep secrets out of ConfigMaps |
| `secrets:` | `Secret` | kompose's conversion table lists `secrets` as supported; external secrets are not |
| named volume | `PersistentVolumeClaim` + `volumeMounts` | kompose creates a PVC; size it with the `kompose.volume.size` label |
| bind mount | usually a ConfigMap (config) or PVC (data) | `hostPath` is almost always wrong in a cluster |
| `depends_on` | nothing | kompose's table marks it unsupported; use readiness probes and `initContainers` |
| `healthcheck:` | probes | kompose has `kompose.service.healthcheck.*` labels for liveness and readiness |
| `restart:` | Deployment for `always`, `unless-stopped` or unset | `on-failure` gives a Pod with `OnFailure`, `no` a Pod with `Never` (kompose restart table; CronJob for scheduled) |
| `deploy.replicas` | `spec.replicas` | |
| `deploy.resources` | `resources.limits` | kompose maps the limits (memory and CPU) |
| `networks:` | flat cluster network + `NetworkPolicy` | kompose supports `networks` but not aliases or addresses |
| `network_mode` | not supported by kompose | share localhost by putting containers in one Pod |
| `links`, `external_links` | not supported by kompose | Services provide DNS names |
| `container_name`, `cap_add` | metadata name, `securityContext.capabilities.add` | |
| `profiles`, `include` | not covered by kompose's table | flatten with `docker compose config` first |

## kompose
```bash
docker compose config > resolved.yaml                       # flatten overrides/profiles/env first
kompose convert -f resolved.yaml --controller deployment
kubectl apply -f . --dry-run=server
```
`--controller` takes `deployment`, `daemonset`, `replicationcontroller` or `statefulset`
(the `kompose.controller.type` label does the same per service). Check `kompose convert --help`
for flags such as chart output or volume type: the user guide does not document them.
Control the output with labels on the Compose service (all listed in the kompose user guide):
```yaml
labels:
  kompose.service.type: LoadBalancer        # or nodeport, clusterip, headless
  kompose.service.expose: "api.example.com" # creates an Ingress
  kompose.service.expose.tls-secret: api-tls
  kompose.volume.size: 20Gi
  kompose.volume.storage-class-name: fast
  kompose.image-pull-secret: regcred
  kompose.controller.type: statefulset      # for databases
  kompose.service.healthcheck.readiness.http_get_path: /ready
  kompose.service.healthcheck.readiness.http_get_port: "8080"
```
Review everything kompose emits. Documented gaps: `depends_on`, `network_mode`, `links` and
network aliases are unsupported; `restart: unless-stopped` is treated like `always`; `deploy`
resources become limits only; `build:` images are built only when you pass `--build` and
pushed only with `--push-image=true` (registry override `--push-image-registry`).

## The hand-fix checklist after convert
1. Replace `hostPath` volumes: config → `ConfigMap`, data → PVC with a `storageClassName`.
2. Split secrets out of the generated ConfigMaps into `Secret` objects (or External
   Secrets / SealedSecrets); never commit the kompose output as-is.
3. Add `readinessProbe` to every HTTP service; keep liveness conservative.
4. Databases: `StatefulSet` with `volumeClaimTemplates`, a headless Service, `replicas: 1`
   unless the DB actually clusters — or move them to a managed service, which is the
   usual reason to be on k8s anyway.
5. `depends_on` ordering: kompose drops it; use an init container (kompose has
   `kompose.init.containers.*` labels) or let readiness probes and retries handle it.
6. Set `resources.requests` as well as limits (kompose maps `deploy.resources` to limits
   only), so the scheduler has real numbers.
7. Ingress + TLS instead of host port publishing; `Service.type: ClusterIP` for internal.
8. Recreate network isolation with `NetworkPolicy` (deny-all default, allow per edge).
9. `imagePullPolicy` and `imagePullSecrets`; pin digests.
10. Put it under `kustomize` or a Helm chart so dev/prod overlays replace the Compose
    override-file habit.

## Alternatives to kompose
- Docker Desktop's Kubernetes (kubeadm or kind provisioner) to test the manifests locally.
- Write the manifests or a Helm chart by hand and port the values over.
- Docker documents "Compose Bridge" for converting Compose files to Kubernetes manifests;
  see the Compose Bridge pages in the Docker docs.

## Verify
```bash
kubectl apply -f k8s/ && kubectl rollout status deploy/api
kubectl get pods,svc,pvc,ingress
kubectl port-forward svc/api 8080:8080     # then request your health endpoint
kubectl get cm -o yaml                      # confirm no passwords or tokens in ConfigMaps
```

## Checked
Date: 2026-10-26. Documentation: kubernetes/kompose docs (user guide and conversion matrix; repository last commit 2026-09-30), kubernetes/website probes, command/args and NetworkPolicy pages, docker/docs Desktop Kubernetes page. Confirmed: the kompose label names, controller values, restart-policy table, unsupported keys (`depends_on`, `network_mode`, `links`), deploy mapping to limits, build/push flags, `command` and `args` equivalence. Removed as unconfirmed: the CLI flags `--volumes`, `--pvc-request-size`, `--secrets-as-files`, `-c`, `-o`, claims about ConfigMap-per-env_file, liveness-only healthcheck mapping, extra Service/strategy behaviour, `hostPath` fallbacks, `kompose.service.expose.tls-secret` retained (documented), the nc init-container example, podman and `helm create` alternatives.
Method: documentation only; no commands were run.
