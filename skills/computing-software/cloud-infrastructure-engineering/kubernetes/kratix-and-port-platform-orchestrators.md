---
id: computing-software.cloud-infrastructure-engineering.kubernetes.kratix-and-port-platform-orchestrators
name: kratix-and-port-platform-orchestrators
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, kratix, port-io, platform-orchestrator, platform-engineering, internal-developer-platform, self-service]
level: advanced
status: docs-checked
description: "Build self-service platform APIs with Kratix Promises (API, pipelines, GitOps destinations) and front them with Port blueprints, the Kubernetes exporter and self-service actions."
sources: ["https://docs.kratix.io/main/reference/promises/intro", "https://docs.kratix.io/main/reference/destinations/intro", "https://github.com/syntasso/kratix-docs/blob/main/docs/main/10-troubleshooting.md", "https://docs.port.io/context-lake/ingestion/ingest-data-into-port/native-integrations/available-integrations/kubernetes-stack/kubernetes/", "https://github.com/port-labs/port-k8s-exporter", "https://docs.port.io/workflows/actions-and-automations/setup-backend/"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Kratix and Port-style platform orchestrators

Two layers of an internal developer platform:
- **Orchestrator** (Kratix, Crossplane, Humanitec): turns a request into infrastructure and config.
- **Portal** (Port, Backstage): catalog and forms where developers make requests and see state.

## Kratix
Runs on a platform cluster. A **Promise** packages a service offering:
```yaml
apiVersion: platform.kratix.io/v1alpha1
kind: Promise
metadata: {name: postgresql}
spec:
  api:                       # a CRD: what developers request
    apiVersion: apiextensions.k8s.io/v1
    kind: CustomResourceDefinition
    metadata: {name: postgresqls.marketplace.acme.io}
    # spec.versions[].schema: size, version, backups ...
  dependencies: []           # resources scheduled to matching destinations (e.g. an operator)
  workflows:
    resource:
      configure:
      - apiVersion: platform.kratix.io/v1alpha1
        kind: Pipeline
        metadata: {name: instance-configure}
        spec:
          containers:
          - name: generate
            image: ghcr.io/acme/pg-promise-pipeline:1.4   # reads /kratix/input/object.yaml, writes /kratix/output/
  destinationSelectors:
  - matchLabels: {environment: dev}
```
Flow: developer applies a `PostgreSQL` request -> Kratix runs the pipeline containers
(policy checks, naming, cost tags, generating manifests) -> documents a container writes to
`/kratix/output` are scheduled to a matching **Destination** and written to its **State
Store** (`GitStateStore` or `BucketStateStore`) -> a GitOps agent such as Flux or Argo CD
on the destination cluster applies them. Pipeline containers are ordinary images, so they can
also call cloud APIs or other tools.
Debug: `kubectl get promises`, the request's `Work`, then
`kubectl get workplacement --selector kratix.io/work=<work-name>` (its `workloads[].content`
is gzip-compressed and base64-encoded), and pipeline pod logs.

## Port
SaaS portal with a typed catalog.
- **Blueprints**: entity schemas (Service, Environment, Cluster, Workload, PostgreSQL).
- **Kubernetes exporter** (installed with Helm in each cluster) maps resources to entities
  with jq:
```yaml
resources:
- kind: apps/v1/deployments
  selector: {query: .metadata.namespace | startswith("kube") | not}
  port:
    entity:
      mappings:
      - identifier: .metadata.name + "-" + .metadata.namespace + "-" + env.CLUSTER_NAME
        title: .metadata.name
        blueprint: '"workload"'
        properties: {replicas: .spec.replicas, image: ".spec.template.spec.containers[0].image"}
```
- **Self-service actions**: forms whose backend is, for example, a GitHub workflow, GitLab
  pipeline, Azure DevOps or Jenkins pipeline, webhook, or Kafka topic. A typical action opens a PR adding a Kratix request (or Crossplane
  claim) to Git; the result flows back into the catalog via the exporter.

## Design rules
- The API (Promise CRD / claim) is the product; keep it small and opinionated.
- Everything ends in Git, so changes are reviewable and reproducible.
- Day-2 actions (resize, delete, rotate credentials) matter as much as create.

## Verify
- [ ] A developer request goes from portal form to running resource with no platform-team
  ticket, and its status is visible back in the portal.

## Checked
2026-10-27, against Kratix docs (syntasso/kratix-docs main: Promise reference, Destinations reference, troubleshooting), the Port Kubernetes exporter default `appConfig.yaml` (port-labs/port-k8s-exporter main) and the Port docs pages for the Kubernetes exporter and action backends. Confirmed: `platform.kratix.io/v1alpha1` `Promise` with `api`, `dependencies`, `workflows.resource.configure` `Pipeline` and `destinationSelectors[].matchLabels`; `/kratix/output` scheduling, `/kratix/input/object.yaml`; Git and Bucket State Stores and Flux/Argo CD as GitOps agents; `Work`/`WorkPlacement` debugging; the exporter `kind`/`selector.query`/`port.entity.mappings` format with `env.CLUSTER_NAME`, Helm installation, and the listed action backends.
Method: documentation only; no commands were run.
