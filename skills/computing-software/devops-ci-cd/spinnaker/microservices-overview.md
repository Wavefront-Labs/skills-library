---
id: computing-software.devops-ci-cd.spinnaker.microservices-overview
name: microservices-overview
category: computing-software
field: devops-ci-cd
product: spinnaker
tags: [architecture, microservices, gate, orca, clouddriver, front50, fiat, echo, igor, rosco]
level: intro
status: docs-checked
description: "Explain what each Spinnaker microservice does (Deck, Gate, Orca, Clouddriver, Front50, Rosco, Igor, Echo, Fiat, Kayenta, Keel)."
sources:
  - https://spinnaker.io/docs/reference/architecture/microservices-overview/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Spinnaker is a set of independent microservices. Knowing the job of each tells you where to look when something fails.

- **Deck** is the browser UI.
- **Gate** is the API gateway. The UI and every API caller talk to Spinnaker only through Gate.
- **Orca** is the orchestration engine and handles all ad-hoc operations and pipelines.
- **Clouddriver** makes all mutating calls to cloud providers and indexes and caches deployed resources.
- **Front50** persists metadata for applications, pipelines, projects and notifications.
- **Rosco** is the bakery. It produces immutable VM images (or image templates) and currently wraps Packer; it also supports helm, kustomize and helmfile bakes for Kubernetes manifests.
- **Igor** triggers pipelines from CI systems such as Jenkins and Travis CI and lets Jenkins/Travis stages run inside pipelines.
- **Echo** is the eventing bus: notifications (Slack, email, SMS) and incoming webhooks from services like GitHub.
- **Fiat** is the authorization service; it answers what a user may access among accounts, applications and service accounts.
- **Kayenta** provides automated canary analysis.
- **Keel** powers Managed Delivery.

Practical reading: a slow cluster view points at Clouddriver, a stuck pipeline at Orca, a lost pipeline definition at Front50, a login or 403 problem at Gate or Fiat, a missing notification at Echo.

## Checked

Method: docs-checked 2026-11-09 against the full spinnaker.io Spinnaker Architecture Overview page (reference/architecture/microservices-overview). Confirmed every service description above, added Rosco's helm, kustomize and helmfile bakes, and removed the Halyard entry, which the current page no longer lists. The last paragraph is an interpretation of those roles, not a quoted rule.
