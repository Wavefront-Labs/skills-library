---
id: computing-software.cloud-infrastructure-engineering.docker.mapping-compose-to-kubernetes-objects
name: mapping-compose-to-kubernetes-objects
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, compose-to-kubernetes, kubernetes-migration, kompose, kompose-convert, healthcheck-to-probes, probes-mapping, volumes-to-pvc, service-vs-ingress, compose-networks-to-services]
level: advanced
description: "Translate Compose services to Kubernetes by hand or with kompose convert: healthchecks to probes, volumes to PVCs, ports and networks to Services, Ingress and NetworkPolicy."
sources: ["https://kompose.io/user-guide/", "https://kompose.io/conversion/", "https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/", "https://kubernetes.io/docs/tasks/inject-data-application/define-command-argument-container/", "https://kubernetes.io/docs/concepts/services-networking/network-policies/"]
status: docs-checked
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Mapping Compose to Kubernetes objects

## kompose convert
```sh
kompose convert -f compose.yaml                          # Deployments, Services, PVCs
kompose convert -f compose.yaml --controller statefulset
```
Steer output with service labels:
```yaml
labels:
  kompose.service.type: LoadBalancer            # or NodePort / ClusterIP / headless
  kompose.service.expose: api.example.com        # generate an Ingress
  kompose.controller.type: statefulset
  kompose.volume.size: 10Gi
  kompose.image-pull-secret: regcred
```
Treat output as a first draft: review every file, then own it as plain manifests/Helm.

## Field-by-field
| Compose | Kubernetes |
|---|---|
| `image`, `command`, `entrypoint` | `containers[].image`; Kubernetes `command` corresponds to ENTRYPOINT and `args` to CMD |
| `environment`, `env_file` | `env` / `envFrom` from ConfigMap; secrets -> Secret |
| `healthcheck` | probes (below) |
| named volume | PersistentVolumeClaim (+ StorageClass, accessModes) |
| bind mount of config | ConfigMap/Secret volume |
| `ports` | Service (ClusterIP) + Ingress/Gateway for HTTP, LoadBalancer for TCP |
| networks | flat cluster network; isolation via NetworkPolicy (kompose supports `networks` but not aliases or addresses) |
| `depends_on` | none (kompose marks it unsupported) - readiness probes, init containers, retry logic |
| `deploy.resources` | `resources.limits` via kompose; add `requests` yourself |
| `restart` | `always`/`unless-stopped`/unset: controller (Always); `on-failure`: Pod (OnFailure); `no`: Pod (Never), per the kompose restart table |
| `secrets` | Secret (kompose: external secrets not supported) |

## Healthcheck -> probes
```yaml
readinessProbe: { httpGet: { path: /ready, port: 8080 }, periodSeconds: 5, failureThreshold: 3 }
livenessProbe:  { httpGet: { path: /healthz, port: 8080 }, periodSeconds: 10, failureThreshold: 3, timeoutSeconds: 2 }
startupProbe:   { httpGet: { path: /healthz, port: 8080 }, periodSeconds: 2, failureThreshold: 60 }   # replaces start_period
```
Kubernetes probes are defined in the Pod spec (`httpGet`, `exec` and gRPC probes are documented);
a Dockerfile HEALTHCHECK is not translated automatically.

## Volumes -> PVCs
- Each named volume -> PVC with an explicit size (`kompose.volume.size`) and storage class
  (`kompose.volume.storage-class-name`); check access modes for volumes shared by several pods.
- Databases -> StatefulSet with `volumeClaimTemplates`.
- Ownership: kompose has a `kompose.security-context.fsgroup` label; the equivalent Kubernetes
  field is `securityContext.fsGroup`.

## Networks -> Services/Ingress/NetworkPolicy
- Every Compose service other services call becomes a ClusterIP Service with the same name
  (DNS compatible within a namespace).
- Published HTTP ports -> Ingress/Gateway routes with TLS, not NodePorts.
- `internal: true` networks -> NetworkPolicies allowing only the intended pods.

## Verify
`kubectl apply --dry-run=server -f k8s/`; `kubectl get pods` ready; endpoints exist for each
Service (`kubectl get endpointslices`).

## Checked
Date: 2026-10-26. Documentation: kubernetes/kompose user guide and conversion matrix (last commit 2026-09-30), kubernetes/website command/args, probes and NetworkPolicy pages. Confirmed: label names, `--controller`, restart table, unsupported `depends_on`, resource limits mapping, secrets support, fsgroup label, probe field names (`httpGet`, `periodSeconds`, `failureThreshold`, `timeoutSeconds`, `startupProbe`), command/args equivalence. Removed as unconfirmed: `-c` and `-o` flags, "Docker HEALTHCHECK is ignored", `tcpSocket` advice, ReadWriteMany examples (NFS/EFS/Filestore), same-name DNS claim.
Method: documentation only; no commands were run.
