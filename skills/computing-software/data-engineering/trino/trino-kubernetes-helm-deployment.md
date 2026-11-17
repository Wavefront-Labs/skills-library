---
id: computing-software.data-engineering.trino.trino-kubernetes-helm-deployment
name: trino-kubernetes-helm-deployment
category: computing-software
field: data-engineering
product: trino
tags: [helm-chart, kubernetes, kind, helm-values, port-forward]
level: practitioner
status: docs-checked
description: "Deploy Trino on Kubernetes with the Helm chart: override heap, workers and catalogs in values YAML, and test locally with kind."
sources: ["https://github.com/trinodb/trino/blob/master/docs/src/main/sphinx/installation/kubernetes.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Trino kubernetes helm deployment

The quickest route is the Trino Helm chart. You need a supported Kubernetes cluster plus kubectl and helm within their version skew policies.

Install:

```text
helm repo add trino https://trinodb.github.io/charts
helm install example-trino-cluster trino/trino
helm install -f example.yaml example-trino-cluster trino/trino
```

Check `kubectl get all`: coordinator and worker pods should be Ready. To use the cluster, tunnel to the coordinator service with `kubectl port-forward svc/trino 8080:8080`, then run `trino --server http://localhost:8080` and a query such as `select count(*) from tpch.tiny.nation;`.

Docs advice: Trino works best with fewer, larger pods; avoid several Trino pods on one physical host.

Override only what you need in YAML:

```yaml
image:
  tag: "<version>"
server:
  workers: 3
coordinator:
  jvm:
    maxHeapSize: "8G"
worker:
  jvm:
    maxHeapSize: "8G"
```

Pin `image.tag`; the default `latest` pulls a new release on each deployment, which is not recommended. Some memory settings outside the heap range stop Trino starting; see the resource management properties warnings. Add catalogs under `catalogs:`, each key a catalog name with its properties as a block, for example `lakehouse` using `connector.name=iceberg` and `hive.metastore.uri=thrift://example.net:9083`.

Local testing: `kind create cluster --name trino`, then pass `--context kind-trino` to kubectl, and `kind delete cluster -n trino` when done. Remove a release with `helm uninstall <name>`, then confirm with `kubectl get all`.

## Checked

2026-11-09: confirmed against the Trino on Kubernetes with Helm page (docs/src/main/sphinx/installation/kubernetes.md): requirements, `helm repo add`, `helm install` with and without `-f`, `kubectl get all` readiness check, `kubectl port-forward svc/trino 8080:8080`, the CLI test query, the fewer-larger-pods advice, the example values (`image.tag`, `server.workers`, `coordinator.jvm.maxHeapSize`, `worker.jvm.maxHeapSize`), the warning on memory settings, the `catalogs` block, the kind commands and `helm uninstall`. The page example of the uninstall uses a release name different from the install example; the skill keeps a placeholder.

Method: documentation only; no commands were run.
