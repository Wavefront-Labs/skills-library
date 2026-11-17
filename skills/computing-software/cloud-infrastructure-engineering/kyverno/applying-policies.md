---
id: computing-software.cloud-infrastructure-engineering.kyverno.applying-policies
name: applying-policies
category: computing-software
field: cloud-infrastructure-engineering
product: kyverno
tags: [applying-policies, admission-webhook, cli-pipeline, gitops-check, json-payload, application-modes]
level: intro
status: docs-checked
description: "Choose where Kyverno policies run: in-cluster admission webhooks, background and cleanup, CI pipelines with the CLI, or on arbitrary JSON via the SDK."
sources:
  - https://kyverno.io/docs/guides/applying-policies/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Three application modes:

- In a cluster: Kyverno is a dynamic admission controller receiving validating and mutating webhook callbacks from the API server. Matching policies enforce admission rules or reject requests. Exceptions can live inside rules or in a separate PolicyException. Cleanup policies delete existing resources on a schedule.
- In pipelines: the CLI checks YAML manifests before they are committed or applied (GitOps-friendly). Use `kyverno apply` for ad-hoc checks and `kyverno test` for predefined cases (see the CLI skills).
- Via APIs: Kyverno JSON, ValidatingPolicy and ImageValidatingPolicy can evaluate any JSON payload through a Go SDK or web service.

Practical order: author with the CLI against sample resources, add `kyverno test` cases in CI, then roll out in the cluster with `Audit` (or `validationActions: [Audit]`) first, read the policy reports, and switch to `Enforce`/`Deny` once results are clean.

The page does not cover kubectl or Helm workflows, namespace scoping or flags; see the installation, configuring, policy-settings and match-and-exclude skills.

## Checked

2026-11-03. Identifiers, flags, Helm values, defaults and version gates in this skill were checked against the official Kyverno documentation pages cited in `sources` (kyverno.io docs, fetched this batch). Where the pages did not document a field, the skill says so or the claim was left out.

Method: documentation only; no commands were run.
