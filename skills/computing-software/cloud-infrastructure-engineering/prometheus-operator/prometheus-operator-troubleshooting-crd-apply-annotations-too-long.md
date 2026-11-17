---
id: computing-software.cloud-infrastructure-engineering.prometheus-operator.prometheus-operator-troubleshooting-crd-apply-annotations-too-long
name: prometheus-operator-troubleshooting-crd-apply-annotations-too-long
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-operator
tags: [crd-annotations-too-long, server-side-apply, argocd-server-side, last-applied-configuration, upgrade-crds]
level: practitioner
status: docs-checked
description: "Fix the metadata.annotations Too long error when applying Prometheus Operator CRDs, using server-side apply."
sources: ["https://prometheus-operator.dev/docs/platform/troubleshooting/", "https://prometheus-operator.dev/docs/platform/operator/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
## Symptom
Applying updated CRDs fails:
```
The CustomResourceDefinition "prometheuses.monitoring.coreos.com" is invalid: metadata.annotations: Too long: must have at most 262144 bytes
```

## Cause
`kubectl apply` runs client-side by default and stores the last-applied configuration in an annotation. For these large CRDs the annotation exceeds the Kubernetes hard limit of 262144 bytes.

## Fix
Use server-side apply, which needs Kubernetes 1.22 or newer:
```bash
kubectl apply --server-side --force-conflicts -f $MANIFESTS
```
`--force-conflicts` takes over fields currently owned by another manager (for example from an earlier client-side apply or a different tool).

## GitOps
With Argo CD, enable its server-side apply sync option (see the Argo CD sync-options documentation) for the application that manages these CRDs.

The operator binary has `crds` and `full-crds` commands that print its CRDs as YAML.

## Checked

2026-11-08. Read the troubleshooting page in full. Removed an unsourced Helm claim and softened the cause wording; crds and full-crds commands re-sourced to the CLI reference.

Method: documentation only; no commands were run.
