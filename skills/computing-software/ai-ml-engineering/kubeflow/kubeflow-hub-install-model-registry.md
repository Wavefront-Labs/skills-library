---
id: computing-software.ai-ml-engineering.kubeflow.kubeflow-hub-install-model-registry
name: kubeflow-hub-install-model-registry
category: computing-software
field: ai-ml-engineering
product: kubeflow
tags: [hub-install, kustomize-overlays, model-registry-service, insecure-skip-verify]
level: practitioner
status: docs-checked
description: "Install the Kubeflow Model Registry on KCD or standalone with kustomize overlays (db, istio, ui, csi), profile namespaces, TLS caveat and health checks."
sources: ["https://github.com/kubeflow/website/blob/master/content/en/docs/components/hub/installation.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Hub install model registry

Requirements: Kubernetes 1.27 or newer, Kustomize 5.0.3 or newer.

On the Kubeflow Community Distribution (opt-in alpha component in KCD 1.9 and later): clone the `hub` repo at the release tag, `cd hub/manifests/kustomize`. By default it deploys into `kubeflow`; to target a user profile namespace run `kustomize edit set namespace $PROFILE_NAME` in `options/istio` and `overlays/db`. Then:

```sh
kubectl apply -k overlays/db
kubectl apply -k options/istio
kubectl apply -k options/ui/overlays/istio
```

Watch pods with `kubectl get pods -n $PROFILE_NAME -w`, then add a Model Registry entry (`/model-registry/`) to the `centraldashboard-config` menuLinks.

Standalone: create the `kubeflow` namespace (or edit the kustomization), then `kubectl apply -n kubeflow -k "https://github.com/kubeflow/hub/manifests/kustomize/overlays/db?ref=v${MODEL_REGISTRY_VERSION}"`. If the cluster uses Istio you must also apply `options/istio`; for KServe to understand `model-registry://` URIs apply the cluster-scoped `options/csi` (a `CustomStorageContainer`).

TLS: for local development with self-signed certificates set `INSECURE_SKIP_VERIFY=true` on the `model-registry-ui` deployment (patch or `kubectl set env`). Never use it in production.

Verify: `kubectl wait --for=condition=available -n kubeflow deployment/model-registry-deployment --timeout=1m`, port-forward `svc/model-registry-service` and call `/api/model_registry/v1alpha3/registered_models`. A non-2xx response may mean a different API version (`v1alphaX`) than the server serves.

## Checked

Confirmed version requirements, the KCD and standalone kustomize steps, the options/istio and options/csi overlays, the INSECURE_SKIP_VERIFY caveat and the verification commands. Nothing removed.

Method: docs-checked 2026-11-09 against the raw kubeflow/website Hub installation.md page, read in full.
