---
id: computing-software.cloud-infrastructure-engineering.k3s.k3s-auto-deploying-manifests
name: k3s-auto-deploying-manifests
category: computing-software
field: cloud-infrastructure-engineering
product: k3s
tags: [k3s, addon, manifests-directory, deploy-controller]
level: practitioner
status: docs-checked
description: "Deploy YAML automatically by placing files in /var/lib/rancher/k3s/server/manifests, tracked as AddOn resources."
sources:
  - https://docs.k3s.io/installation/packaged-components
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: apply manifests declaratively on server nodes.

Any file in /var/lib/rancher/k3s/server/manifests is deployed to Kubernetes similarly to `kubectl apply`, at startup and whenever the file changes. Deleting a file does not delete the resources it created.

Manifests are tracked as AddOn custom resources in the kube-system namespace. For errors or warnings use `kubectl describe` on the AddOn, or `kubectl get event -n kube-system`.

Packaged components deployed this way: coredns, traefik, local-storage and metrics-server. The embedded servicelb controller has no manifest but can be disabled as if it were an AddOn. K3s manages these manifests and rewrites them on every start, so do not alter them.

User AddOns: each file may hold multiple resources separated by `---`.

Naming: the AddOn name comes from the file basename. Names must be unique (including inside subdirectories), follow Kubernetes object naming, and avoid conflicts with packaged component names even when those are disabled. A file such as example_manifest.yaml fails with an Addon invalid error because underscores are not allowed in a lowercase RFC 1123 subdomain.

Danger: with multiple servers, K3s does not sync AddOn files between nodes. Keeping files identical is your job; K3s cannot guarantee correct behavior if servers deploy conflicting manifests.

## Checked

2026-11-08. Read the full K3s Managing Packaged Components page (docs/installation/packaged-components.md in the k3s-io/docs repo). Confirmed: the manifests directory, kubectl apply-like deployment, deletion not removing resources, AddOn resources in kube-system, packaged component list, servicelb without a manifest, rewrite on start, multi-document files, naming rules with the underscore error, and the multi-server sync warning. Reworded the last sentence to match the page.

Method: documentation only; no commands were run.
