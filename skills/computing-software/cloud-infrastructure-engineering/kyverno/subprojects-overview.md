---
id: computing-software.cloud-infrastructure-engineering.kyverno.subprojects-overview
name: subprojects-overview
category: computing-software
field: cloud-infrastructure-engineering
product: kyverno
tags: [subprojects, chainsaw, policy-reporter, kyverno-json, kyverno-authz, backstage-plugin]
level: intro
status: docs-checked
description: "Know the Kyverno sub-projects and their maturity: CLI, Kyverno JSON, Authz Server, Chainsaw, Policy Reporter and the Backstage plugin, with where their docs live."
sources:
  - https://kyverno.io/docs/subprojects/chainsaw/
  - https://kyverno.io/docs/subprojects/policy-reporter/
  - https://kyverno.io/docs/subprojects/kyverno-json/
  - https://kyverno.io/docs/subprojects/authz/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The docs list six sub-projects: Kyverno CLI, Kyverno JSON, Authz Server, Chainsaw, Policy Reporter and Backstage Plugin. The pages read are short landing stubs with no install or config detail.

- Chainsaw: declarative end-to-end testing for Kubernetes controllers; marked Beta. Use it for cluster-level policy tests (when migrating to CEL, update its policy types and status checks).
- Policy Reporter: in-cluster management of policy reports with a web UI; marked Stable. Docs at kyverno.github.io/policy-reporter-docs, source github.com/kyverno/policy-reporter.
- Kyverno JSON: applies policies to non-Kubernetes workloads, any JSON payload; the page marks it deprecated. Site kyverno.github.io/kyverno-json.
- Authz Server: policy-based authorization for Envoy proxies and HTTP services; Alpha, since Kyverno v0.4.0. Site kyverno.github.io/kyverno-authz. The CLI can test it with `kyverno apply --envoy-payload` and `--http-payload`.
- Kyverno CLI: `kyverno apply`, `test`, `jp`, `create`, `json scan`, `migrate`, `version` (see the CLI skills).

For the JSON-payload route inside the main project, ValidatingPolicy and ImageValidatingPolicy can evaluate JSON through a Go SDK or web service (applying-policies page).

Unverified from these pages: install steps, CRDs, flags and policy kinds for each sub-project.

## Checked

2026-11-03. Identifiers, flags, Helm values, defaults and version gates in this skill were checked against the official Kyverno documentation pages cited in `sources` (kyverno.io docs, fetched this batch). Where the pages did not document a field, the skill says so or the claim was left out.

Method: documentation only; no commands were run.
