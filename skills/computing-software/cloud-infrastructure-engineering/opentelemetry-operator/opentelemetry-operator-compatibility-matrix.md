---
id: computing-software.cloud-infrastructure-engineering.opentelemetry-operator.opentelemetry-operator-compatibility-matrix
name: opentelemetry-operator-compatibility-matrix
category: computing-software
field: cloud-infrastructure-engineering
product: opentelemetry-operator
tags: [opentelemetry-operator, compatibility, kubernetes-versions, collector-version-tracking, go-support-policy, prometheus-operator-version]
level: practitioner
status: docs-checked
description: "Check which Kubernetes, cert-manager and prometheus-operator versions an operator release supports, and how operator and Collector versions track each other."
sources: ["https://github.com/open-telemetry/opentelemetry-operator/blob/main/docs/getting-started/compatibility.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Operator compatibility and version policy

Version tracking: the operator follows the Collector's version up to the minor part. Operator v0.18.1 tracks Collector 0.18.0; the patch number is the operator's own patch level, and a new Collector patch release triggers a new operator patch release. By default the operator creates Collector workloads at the same version as itself (operator 0.40.0 creates Collector 0.40.0).

When `spec.image` is set to a custom image the operator does not manage that Collector's version or upgrades. Best practice is then to keep the operator on the same version as the Collector core your image is based on.

Kubernetes policy: the operator always supports every version maintained upstream, tries to support versions offered by popular distributions (OpenShift and AWS EKS are named), and gives at least one month's notice before dropping a Kubernetes version.

Go policy: the first release after a new Go minor version N adds build and test steps for N, and removes support for N-2. Dropping an unsupported Go version is not treated as a breaking change.

The matrix in the doc lists per operator release the Kubernetes range, cert-manager (v1 throughout) and the prometheus-operator package version the Target Allocator ships with. For example, v0.162.0 lists Kubernetes v1.25 to v1.37 and prometheus-operator v0.94.1, and v0.133.0 is marked N/A. The operator might work outside the ranges, but test on a supported version before filing an issue. Prometheus-operator CRD features used by the Target Allocator are generally backwards compatible, but specific features need the matching package version.

## Checked

2026-11-04. Confirmed against docs/getting-started/compatibility.md: operator-to-Collector version tracking up to the minor part (v0.18.1 tracks 0.18.0), default same-version Collector workloads (0.40.0 example), the custom `spec.image` rule, the Kubernetes policy (all upstream-maintained versions, OpenShift and AWS EKS named, one month's notice), the Go policy (add N, remove N-2, not a breaking change), the cert-manager and prometheus-operator matrix columns, the v0.162.0 row (Kubernetes v1.25 to v1.37, prometheus-operator v0.94.1) and the N/A row for v0.133.0. The matrix is a snapshot of the main branch; check the page for newer releases. Nothing removed.

Method: documentation only; no commands were run.
