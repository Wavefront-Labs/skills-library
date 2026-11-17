---
id: computing-software.ai-ml-engineering.kserve.kserve-localmodel-install
name: kserve-localmodel-install
category: computing-software
field: ai-ml-engineering
product: kserve
tags: [localmodel, kserve-localmodel-crd, kserve-localmodel-resources, localmodel-controller, localmodelnode-agent, kservelocalmodel, addon]
level: practitioner
status: docs-checked
description: "Install the optional LocalModel add-on (after KServe): Kustomize addon overlay or two Helm charts, InferenceService-only support, uninstall and cleanup including the node label."
sources: ["https://github.com/kserve/website/blob/main/docs/install/localmodel-install.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# LocalModel controller installation

LocalModel is an optional add-on and MUST be installed after the KServe controller. It supports InferenceService only (LLMInferenceService support is planned). Components: controller (cache lifecycle and policies) and an agent DaemonSet on worker nodes.

```bash
# Kustomize (from a KServe clone)
kubectl apply -k config/overlays/addons/localmodel

# Helm
helm install kserve-localmodel-crd oci://ghcr.io/kserve/charts/kserve-localmodel-crd \
  --version v0.20.0 --namespace kserve --create-namespace
helm install kserve-localmodel-resources oci://ghcr.io/kserve/charts/kserve-localmodel-resources \
  --version v0.20.0 --namespace kserve --create-namespace --wait
```

Chart values (node selector, resource limits, storage) are in the `kserve-localmodel-resources` chart README.

## Uninstall
```bash
helm uninstall kserve-localmodel-resources -n kserve
helm uninstall kserve-localmodel-crd -n kserve
# or: kubectl delete -k config/overlays/addons/localmodel
```

Cleanup:
```bash
kubectl label nodes -l kserve/localmodel=worker kserve/localmodel-
kubectl delete localmodelcache --all
kubectl delete localmodelnodegroup --all
```

The page's cleanup step removes the node label `kserve/localmodel=worker`; node selection settings are in the chart README, so check there for the agent's default nodeSelector. See the model cache skill for the CRDs.

## Checked
Confirmed against the KServe LocalModel Installation page: install-after-KServe requirement, InferenceService-only support, controller and agent DaemonSet components, the Kustomize and two Helm chart installs, uninstall commands and the cleanup commands. Removed the claim that the agent DaemonSet defaults to a `kserve/localmodel: worker` nodeSelector and that nodes must be labelled, which the page does not state.

Method: docs-only read of cited pages, 2026-11-08
