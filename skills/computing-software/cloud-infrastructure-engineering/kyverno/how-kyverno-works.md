---
id: computing-software.cloud-infrastructure-engineering.kyverno.how-kyverno-works
name: how-kyverno-works
category: computing-software
field: cloud-infrastructure-engineering
product: kyverno
tags: [architecture, admission-controller, engine, background-controller, report-controllers, updaterequest]
level: intro
status: docs-checked
description: "Map Kyverno's components (webhook, engine, webhook and report controllers, background controller, cert renewer) and the request flow from API server to allow or reject."
sources:
  - https://kyverno.io/docs/introduction/how-kyverno-works/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Kyverno runs in the cluster as a dynamic admission controller.

Components:
- Webhook: receives AdmissionReview requests from the API server and hands them to the Engine.
- Engine: evaluates policies and returns admit or reject.
- Webhook Controller: watches installed policies and reconfigures the webhooks so they request only matching resources.
- Cert Renewer: renews the webhook certificates stored as Secrets.
- Background Controller: handles generate and mutate-existing policies by reconciling `UpdateRequest` resources (an intermediary).
- Report Controllers: build Policy Reports from Admission Reports and Background Scan Reports.

Flow: API server, webhook, engine, allow or reject. Enforcement is recorded as Kubernetes events. Allowed requests and resources that existed before a policy show up in Policy Reports with their status. Kyverno also runs runtime scans of matching resources.

Matching uses kind, name, label selectors and other criteria. Mutation uses Kustomize-style overlays or RFC 6902 JSON Patch; validation uses overlay-style patterns and if-then-else conditions (legacy rule syntax).

Other interfaces: the CLI applies policies to clusters or files (Kubernetes manifests, Terraform JSON plans, Dockerfiles); an authorization server handles Envoy and HTTP payloads as a central service or sidecar; an SDK embeds engines in your own app.

HA depends on the controller, and extra replicas may also add scalability. The page says nothing about webhook failure behaviour or the Cleanup controller.

## Checked

2026-11-03. Identifiers, flags, Helm values, defaults and version gates in this skill were checked against the official Kyverno documentation pages cited in `sources` (kyverno.io docs, fetched this batch). Where the pages did not document a field, the skill says so or the claim was left out.

Method: documentation only; no commands were run.
