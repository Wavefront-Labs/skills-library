---
id: computing-software.cloud-infrastructure-engineering.rook.external-cluster-consumer-import
name: external-cluster-consumer-import
category: computing-software
field: cloud-infrastructure-engineering
product: rook
tags: [import-external-cluster, cluster-external-yaml, values-external, kubecontext, connected]
level: advanced
status: docs-checked
description: "Install Rook in a consumer cluster with Helm or manifests, import the provider data with import-external-cluster.sh, and verify the Connected state."
sources:
  - https://rook.io/docs/rook/latest-release/CRDs/Cluster/external-cluster/consumer-import/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Install Rook in the consumer cluster, either way.

Helm: install the `rook-ceph` operator chart, then the cluster chart with the external example values, then the CSI drivers chart:
```
helm install --create-namespace --namespace rook-ceph rook-ceph-cluster \
  --set operatorNamespace=rook-ceph rook-release/rook-ceph-cluster -f values-external.yaml
```
Manifests:
```
kubectl create -f crds.yaml -f common.yaml -f csi-operator.yaml
kubectl create -f operator.yaml -f common-external.yaml -f cluster-external.yaml
```

Import the provider data:
1. Paste the bash output of the export script into your shell.
2. The import script uses the current kubeconfig context; set `KUBECONTEXT=<cluster-name>` to target another cluster.
3. The script defaults to namespace rook-ceph; if the external cluster uses another namespace, change `NAMESPACE=${NAMESPACE:="new-namespace"}` in the script.
4. If nodes run kernel 5.4 or earlier, remove `fast-diff`, `object-map`, `deep-flatten` and `exclusive-lock` from the `imageFeatures` line.
5. Run `. import-external-cluster.sh`.

Verify with `kubectl -n rook-ceph get CephCluster`: the example shows `rook-ceph-external` with state `Connected` and health `HEALTH_OK`. Then check that storage classes exist for the RBD pools and CephFS filesystems you exported.

## Checked

2026-11-03. Read the Rook docs page(s) cited in sources (consumer-import) against this skill: 22 backticked identifiers, flags, versions and quoted strings were matched to the page text; the 0 reported as not literally matched are YAML nesting or placeholder formatting, and each was confirmed by reading the surrounding page text (nested field lists, example output, command blocks). Nothing needed removing.

Method: documentation only; no commands were run.
