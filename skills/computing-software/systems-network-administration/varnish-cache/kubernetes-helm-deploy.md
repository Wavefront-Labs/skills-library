---
id: computing-software.systems-network-administration.varnish-cache.kubernetes-helm-deploy
name: kubernetes-helm-deploy
category: computing-software
field: systems-network-administration
product: varnish-cache
tags: [kubernetes, helm, helm-chart, configmap-vcl]
level: practitioner
status: docs-checked
description: "Deploy Varnish on Kubernetes with the official Helm chart: backend via env vars, inline VCL in server.vclConfig, VCL from a ConfigMap, service type and ingress."
sources:
  - https://www.varnish.org/docs/install-guide/install-kubernetes/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# kubernetes helm deploy

```bash
helm install varnish oci://docker.io/varnish/varnish-cache
helm install varnish -f values.yaml oci://docker.io/varnish/varnish-cache
```

The chart deploys to the cluster in your kubectl active context (`kubectl config current-context` shows it). Default values exist; a values.yaml overrides them.

Backend: the chart's shortcuts `VARNISH_BACKEND_HOST` and `VARNISH_BACKEND_PORT` (the service Varnish fetches from), set in values.yaml:

```yaml
server:
  extraEnvs:
    VARNISH_BACKEND_HOST: "example.default.svc.cluster.local"
    VARNISH_BACKEND_PORT: "80"
```

or `--set server.extraEnvs.VARNISH_BACKEND_HOST=... --set server.extraEnvs.VARNISH_BACKEND_PORT=80`.

Inline VCL: put the whole VCL (with its own `backend default`) in `server.vclConfig: |`. The page's example passes `/admin` URLs and sets `bereq.http.Host`.

VCL from a ConfigMap (described as cleaner and more flexible):

```bash
kubectl create configmap external-vcl --from-file=./default.vcl
```

```yaml
server:
  vclConfig: ""   # must be unset to override default.vcl
  extraVolumes:
    - name: external
      configMap:
        name: external-vcl
  extraVolumeMounts:
    - name: external
      mountPath: /etc/varnish/default.vcl
      subPath: default.vcl
```

Then `helm install varnish -f values.yaml oci://docker.io/varnish/varnish-cache`.

Exposure: the chart exposes a NodePort service by default; set `server.service.type` to `ClusterIP` or `LoadBalancer` (values.yaml or `--set server.service.type=ClusterIP`). Ingress: `server.ingress` with `enabled: true`, `ingressClassName` (the page uses nginx), `pathType: Prefix` and `hosts` entries; test with `curl -H"Host: varnish.example.com" http://localhost`.

## Checked

Method: 2026-11-08 docs-only read of the cited install guide. Earlier claims matched; added the default NodePort, service type and ingress sections that were missing.
